from __future__ import annotations

import asyncio
import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, Literal

from agent.providers.geminiProviders import GeminiProvider
from agent.skills import SkillsManager
from agent.tools.registry import ToolRegistry
from agent.tools.visualization_tools import ShowWidgetTool, VisualizeReadMeTool

logger = logging.getLogger("genui.agent")


@dataclass
class ChatMessage:
    id: str
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: str


@dataclass
class ChatSession:
    id: str
    messages: list[ChatMessage] = field(default_factory=list)


class GenUIAgentService:
    def __init__(self) -> None:
        self.sessions: Dict[str, ChatSession] = {}
        self.sessions_dir = Path(__file__).resolve().parent.parent.parent / "frontend" / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        guidelines_dir = (
            Path(__file__).resolve().parent.parent
            / "reference"
            / "pi-generative-ui"
            / ".pi"
            / "extensions"
            / "generative-ui"
            / "claude-guidelines"
        )
        self.available_modules = ["interactive", "chart", "mockup", "art", "diagram"]
        self.guideline_file_by_module: dict[str, Path] = {
            "interactive": guidelines_dir / "interactive.md",
            "chart": guidelines_dir / "chart.md",
            "mockup": guidelines_dir / "mockup.md",
            "art": guidelines_dir / "art.md",
            "diagram": guidelines_dir / "diagram.md",
        }
        self.skills = SkillsManager.default()
        self.tools = ToolRegistry()
        self.tools.register(
            VisualizeReadMeTool(
                available_modules=self.available_modules,
                guideline_file_by_module=self.guideline_file_by_module,
            )
        )
        self.tools.register(
            ShowWidgetTool(
                available_modules=self.available_modules,
                progressive_payloads=self._progressive_widget_payloads,
            )
        )

    def ensure_session(self, session_id: str | None) -> ChatSession:
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]
        if session_id:
            loaded = self._load_session_from_disk(session_id)
            if loaded is not None:
                self.sessions[loaded.id] = loaded
                return loaded
        created = ChatSession(id=session_id or str(uuid.uuid4()))
        self.sessions[created.id] = created
        self._persist_session(created)
        return created

    def append_message(self, session: ChatSession, message: ChatMessage) -> None:
        session.messages.append(message)
        self._persist_session(session)

    def get_session(self, session_id: str) -> ChatSession | None:
        if session_id in self.sessions:
            return self.sessions[session_id]
        loaded = self._load_session_from_disk(session_id)
        if loaded is None:
            return None
        self.sessions[loaded.id] = loaded
        return loaded

    def list_session_summaries(self) -> list[dict[str, Any]]:
        sessions_by_id: dict[str, ChatSession] = dict(self.sessions)
        for file_path in sorted(self.sessions_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            session_id = file_path.stem
            if session_id in sessions_by_id:
                continue
            loaded = self._load_session_from_disk(session_id)
            if loaded is not None:
                sessions_by_id[session_id] = loaded

        summaries: list[dict[str, Any]] = []
        for session in sessions_by_id.values():
            if session.messages:
                last_message = session.messages[-1]
                updated_at = last_message.created_at
                preview = last_message.content[:80]
            else:
                updated_at = ""
                preview = ""
            summaries.append(
                {
                    "session_id": session.id,
                    "message_count": len(session.messages),
                    "updated_at": updated_at,
                    "preview": preview,
                }
            )
        summaries.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        return summaries

    def stream_reply(
        self,
        session: ChatSession,
        user_text: str,
    ) -> Generator[dict[str, Any], None, str]:
        api_key, key_source = self._resolve_api_key()
        logger.warning(
            "stream_reply start session_id=%s key_source=%s key_present=%s user_text=%s",
            session.id,
            key_source,
            bool(api_key),
            user_text,
        )
        if not api_key:
            logger.error("fallback active: no GEMINI_API_KEY/GOOGLE_API_KEY found in backend process env")
            return (yield from self._stream_fallback(user_text))
        logger.warning("provider mode active model=%s", os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview"))
        return (yield from self._stream_provider(session=session, user_text=user_text, api_key=api_key))

    def _stream_fallback(self, user_text: str) -> Generator[dict[str, Any], None, str]:
        collected: list[str] = []
        include_widget = self._should_stream_widget(user_text)
        for delta in self._simulate_text_intro(user_text, include_widget):
            collected.append(delta)
            yield {"type": "assistant_delta", "delta": delta}
        if include_widget:
            tool_call_id = str(uuid.uuid4())
            widget_code = self._build_widget_html()
            widget_type = self._infer_widget_type(user_text)
            yield {
                "type": "toolcall_start",
                "tool_call_id": tool_call_id,
                "name": "show_widget",
                "widget_type": widget_type,
                "title": "compound_interest_demo",
                "width": 780,
                "height": 520,
                "loading_messages": self._default_loading_messages(user_text),
            }
            for partial in self._progressive_widget_payloads(widget_code):
                yield {"type": "toolcall_delta", "tool_call_id": tool_call_id, "widget_code": partial}
                time.sleep(0.03)
            yield {"type": "toolcall_end", "tool_call_id": tool_call_id, "widget_code": widget_code}
        return "".join(collected)

    def _stream_provider(
        self,
        session: ChatSession,
        user_text: str,
        api_key: str,
    ) -> Generator[dict[str, Any], None, str]:
        visual_request = self._should_stream_widget(user_text)
        visual_flow_started = False
        show_widget_emitted = False
        has_loaded_guidelines = False
        provider = GeminiProvider(
            api_key=api_key,
            default_model=os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview"),
        )
        messages = self._build_provider_messages(session, user_text)
        tools = self.tools.get_definitions()
        assistant_text_chunks: list[str] = []

        for _ in range(5):
            tool_choice = "required" if (visual_request and not show_widget_emitted) else "auto"
            response = asyncio.run(
                provider.chat(
                    messages=messages,
                    tools=tools,
                    model=os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview"),
                    temperature=0.3,
                    max_tokens=4096,
                    tool_choice=tool_choice,
                )
            )
            logger.warning(
                "provider response finish_reason=%s has_tool_calls=%s content_len=%s",
                response.finish_reason,
                bool(response.tool_calls),
                len(response.content or ""),
            )
            if response.finish_reason == "error":
                fallback_text = response.content or response.error or "LLM error"
                logger.error("provider error -> %s", fallback_text)
                safe_text = "模型服务暂时不稳定，请重试。若持续失败，请检查网络或稍后再试。"
                for delta in self._stream_text_chunks(safe_text):
                    assistant_text_chunks.append(delta)
                    yield {"type": "assistant_delta", "delta": delta}
                return "".join(assistant_text_chunks)

            assistant_content = response.content or ""
            if (visual_request or visual_flow_started) and not response.tool_calls and not show_widget_emitted:
                logger.error("visual request received no tool calls, injecting corrective turn")
                messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_content or None,
                        "provider_specific_fields": response.provider_specific_fields,
                    }
                )
                messages.append(
                    {
                        "role": "user",
                        "content": "You must call visualize_read_me and then show_widget for this request. Do not answer with prose only.",
                    }
                )
                continue

            if assistant_content:
                for delta in self._stream_text_chunks(assistant_content):
                    assistant_text_chunks.append(delta)
                    yield {"type": "assistant_delta", "delta": delta}

            if not response.tool_calls:
                return "".join(assistant_text_chunks)

            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_content or None,
                    "tool_calls": [call.to_openai_tool_call() for call in response.tool_calls],
                    "provider_specific_fields": response.provider_specific_fields,
                }
            )

            for tool_call in response.tool_calls:
                logger.warning("tool call name=%s id=%s", tool_call.name, tool_call.id)
                if tool_call.name == "visualize_read_me":
                    visual_flow_started = True
                    has_loaded_guidelines = True
                if tool_call.name == "show_widget" and not has_loaded_guidelines:
                    logger.error("show_widget blocked: visualize_read_me not called yet")
                    messages.append(
                        {
                            "role": "tool",
                            "name": "show_widget",
                            "content": "READ_ME_REQUIRED",
                        }
                    )
                    messages.append(
                        {
                            "role": "user",
                            "content": "Before show_widget, call visualize_read_me with relevant modules, then retry show_widget with i_have_seen_read_me=true.",
                        }
                    )
                    continue
                if tool_call.name == "show_widget" and show_widget_emitted:
                    logger.warning("duplicate show_widget skipped after first successful render")
                    messages.append(
                        {
                            "role": "tool",
                            "name": "show_widget",
                            "content": "SHOW_WIDGET_ALREADY_EMITTED",
                        }
                    )
                    messages.append(
                        {
                            "role": "user",
                            "content": "Do not call show_widget again in this turn. Continue with plain assistant text only.",
                        }
                    )
                    continue
                tool_call_id = tool_call.id or str(uuid.uuid4())
                tool_arguments = dict(tool_call.arguments)
                if tool_call.name == "show_widget":
                    tool_arguments.setdefault("i_have_seen_read_me", has_loaded_guidelines)
                    tool_arguments.setdefault("loading_messages", self._default_loading_messages(user_text))
                execution = self.tools.execute(tool_call.name, tool_arguments, tool_call_id)
                logger.warning(
                    "tool execution name=%s events=%s content_len=%s",
                    tool_call.name,
                    len(execution.events),
                    len(execution.content or ""),
                )
                if tool_call.name == "show_widget" and execution.content == "READ_ME_REQUIRED":
                    logger.error("show_widget rejected: READ_ME_REQUIRED")
                    messages.append(
                        {
                            "role": "tool",
                            "name": tool_call.name,
                            "content": "READ_ME_REQUIRED",
                        }
                    )
                    messages.append(
                        {
                            "role": "user",
                            "content": "Call visualize_read_me first and retry show_widget with i_have_seen_read_me=true.",
                        }
                    )
                    continue
                if tool_call.name == "show_widget" and execution.content == "INVALID_WIDGET_CODE":
                    logger.error("invalid widget code detected, requesting regeneration")
                    messages.append(
                        {
                            "role": "tool",
                            "name": tool_call.name,
                            "content": "INVALID_WIDGET_CODE",
                        }
                    )
                    messages.append(
                        {
                            "role": "user",
                            "content": "Regenerate show_widget with complete interactive HTML including script and controls.",
                        }
                    )
                    continue
                if tool_call.name == "show_widget" and execution.events:
                    show_widget_emitted = True
                for event in execution.events:
                    yield event
                    if event.get("type") == "toolcall_delta":
                        time.sleep(0.03)
                messages.append(
                    {
                        "role": "tool",
                        "name": tool_call.name,
                        "content": execution.content,
                    }
                )

        if visual_request and not show_widget_emitted:
            fallback_text = "本次可视化生成未成功输出组件，我已记录日志。请重试一次，或把需求再具体一些（数据结构、交互方式、配色）。"
            for delta in self._stream_text_chunks(fallback_text):
                assistant_text_chunks.append(delta)
                yield {"type": "assistant_delta", "delta": delta}
        return "".join(assistant_text_chunks)

    def _build_provider_messages(self, session: ChatSession, user_text: str) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = [{"role": "system", "content": self.skills.build_system_prompt()}]
        for msg in session.messages:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": user_text})
        return messages

    def _stream_text_chunks(self, text: str, delay: float = 0.008) -> Generator[str, None, None]:
        if not text:
            return
        for token in text:
            yield token
            if delay > 0:
                time.sleep(delay)

    def _resolve_api_key(self) -> tuple[str, str]:
        for key_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
            value = os.getenv(key_name, "").strip()
            if value:
                return value, key_name
        dotenv_values = self._read_backend_dotenv()
        for key_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
            value = dotenv_values.get(key_name, "").strip()
            if value:
                return value, f".env:{key_name}"
        return "", "none"

    def _read_backend_dotenv(self) -> dict[str, str]:
        dotenv_path = Path(__file__).resolve().parent.parent / ".env"
        if not dotenv_path.exists():
            return {}
        values: dict[str, str] = {}
        try:
            for raw in dotenv_path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key:
                    values[key] = value
        except Exception as exc:
            logger.error("failed to read backend .env file: %s", exc)
            return {}
        return values

    def _session_file(self, session_id: str) -> Path:
        return self.sessions_dir / f"{session_id}.json"

    def _load_session_from_disk(self, session_id: str) -> ChatSession | None:
        file_path = self._session_file(session_id)
        if not file_path.exists():
            return None
        try:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
            raw_messages = payload.get("messages", [])
            messages: list[ChatMessage] = []
            for item in raw_messages:
                if not isinstance(item, dict):
                    continue
                role = str(item.get("role", "user"))
                if role not in ("user", "assistant", "system"):
                    continue
                messages.append(
                    ChatMessage(
                        id=str(item.get("id", str(uuid.uuid4()))),
                        role=role,
                        content=str(item.get("content", "")),
                        created_at=str(item.get("created_at", "")),
                    )
                )
            return ChatSession(id=session_id, messages=messages)
        except Exception as exc:
            logger.error("failed to load session file %s: %s", file_path, exc)
            return None

    def _persist_session(self, session: ChatSession) -> None:
        payload = {
            "session_id": session.id,
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at,
                }
                for msg in session.messages
            ],
        }
        file_path = self._session_file(session.id)
        try:
            file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            logger.error("failed to persist session %s: %s", session.id, exc)

    def _should_stream_widget(self, user_text: str) -> bool:
        normalized = user_text.lower()
        triggers = [
            "visual",
            "widget",
            "chart",
            "diagram",
            "interactive",
            "simulation",
            "dashboard",
            "graph",
        ]
        return any(token in normalized for token in triggers)

    def _infer_widget_type(self, user_text: str) -> Literal["interactive", "chart", "mockup", "art", "diagram"]:
        normalized = user_text.lower()
        if any(token in normalized for token in ["chart", "graph", "plot", "histogram", "timeseries"]):
            return "chart"
        if any(token in normalized for token in ["diagram", "architecture", "flow", "workflow"]):
            return "diagram"
        if any(token in normalized for token in ["mockup", "form", "layout", "ui"]):
            return "mockup"
        if any(token in normalized for token in ["art", "illustration", "draw", "creative"]):
            return "art"
        return "interactive"

    def _simulate_text_intro(self, user_text: str, include_widget: bool) -> Generator[str, None, None]:
        if include_widget:
            reply = (
                f"我将为“{user_text}”生成一个可交互可视化。"
                "你会先看到说明文本流，然后看到 show_widget 的增量渲染事件。"
            )
        else:
            reply = (
                f"已收到你的消息：“{user_text}”。"
                "当前是文本流模式，你可以输入与可视化相关的问题触发工具事件流。"
            )
        for token in reply:
            yield token
            time.sleep(0.01)

    def _default_loading_messages(self, user_text: str) -> list[str]:
        widget_type = self._infer_widget_type(user_text)
        if widget_type == "chart":
            return ["Preparing chart structure", "Binding chart data", "Rendering chart interactions"]
        if widget_type == "diagram":
            return ["Preparing diagram layout", "Routing connectors", "Rendering final diagram"]
        if widget_type == "mockup":
            return ["Preparing mockup layout", "Applying component styles", "Rendering UI interactions"]
        if widget_type == "art":
            return ["Preparing art composition", "Applying visual layers", "Rendering final illustration"]
        return ["Preparing interactive layout", "Binding controls", "Rendering interactive widget"]

    def _build_widget_html(self) -> str:
        return """
<style>
  *{box-sizing:border-box}
  .panel{font-family:Inter,Arial,sans-serif;border:1px solid #d1d5db;border-radius:12px;padding:16px;background:#fff}
  .title{font-size:16px;font-weight:600;color:#111827;margin:0 0 8px}
  .row{display:flex;align-items:center;gap:12px;margin-bottom:12px}
  .hint{font-size:13px;color:#4b5563}
  .value{font-size:14px;font-weight:600;color:#111827;min-width:52px}
  .bar{height:12px;border-radius:9999px;background:#e5e7eb;overflow:hidden}
  .bar > span{display:block;height:100%;background:#2563eb;transition:width .15s ease}
</style>
<div class="panel">
  <p class="title">Compound interest simulator</p>
  <div class="row">
    <span class="hint">Rate (%)</span>
    <input id="rate" type="range" min="1" max="20" value="8" />
    <span id="rateValue" class="value">8%</span>
  </div>
  <div class="row">
    <span class="hint">Years</span>
    <input id="years" type="range" min="1" max="30" value="10" />
    <span id="yearsValue" class="value">10y</span>
  </div>
  <div class="hint">Future value (principal=1000): <span id="fv" class="value">2159</span></div>
  <div class="bar" style="margin-top:10px"><span id="progress" style="width:52%"></span></div>
</div>
<script>
  const principal = 1000;
  const rateEl = document.getElementById('rate');
  const yearsEl = document.getElementById('years');
  const rateValue = document.getElementById('rateValue');
  const yearsValue = document.getElementById('yearsValue');
  const fv = document.getElementById('fv');
  const progress = document.getElementById('progress');
  function recalc(){
    const rate = Number(rateEl.value);
    const years = Number(yearsEl.value);
    const value = Math.round(principal * Math.pow(1 + rate / 100, years));
    rateValue.textContent = rate + '%';
    yearsValue.textContent = years + 'y';
    fv.textContent = String(value);
    const pct = Math.min(100, Math.round(((value - principal) / principal) * 30));
    progress.style.width = pct + '%';
  }
  rateEl.addEventListener('input', recalc);
  yearsEl.addEventListener('input', recalc);
  recalc();
</script>
""".strip()

    def _progressive_widget_payloads(self, code: str, steps: int = 9) -> Iterable[str]:
        if not code:
            return []
        fragments: list[str] = []
        last = ""
        for i in range(1, steps + 1):
            cut = max(24, int(len(code) * i / steps))
            fragment = code[:cut]
            if fragment != last:
                fragments.append(fragment)
                last = fragment
        if fragments[-1] != code:
            fragments.append(code)
        return fragments
