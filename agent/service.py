"""GenUI agent service: thin facade composing core, skills, and providers."""

from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path
from typing import Any, Generator, Iterable, Literal

from agent.core.agent import AgentLoop
from agent.core.config import resolve_config
from agent.core.session import ChatMessage, ChatSession, SessionStore  # noqa: F401
from agent.skills.generative_ui.orchestrator import GenerativeUIOrchestrator
from agent.skills.generative_ui.tools.show_widget import ShowWidgetTool
from agent.skills.generative_ui.tools.visualize_read_me import VisualizeReadMeTool
from agent.skills.loader import build_system_prompt, load_skills
from agent.tools.registry import ToolRegistry

logger = logging.getLogger("genui.agent")


class GenUIAgentService:
    def __init__(self) -> None:
        agent_dir = Path(__file__).resolve().parent

        self.sessions = SessionStore(
            sessions_dir=agent_dir.parent.parent / "frontend" / "sessions"
        )

        guidelines_dir = agent_dir / "guidelines"
        available_modules = [
            "interactive", "chart", "chart_interactive",
            "mockup", "art", "art_interactive", "diagram",
        ]
        guideline_file_by_module: dict[str, Path] = {
            m: guidelines_dir / f"{m}.md" for m in available_modules
        }
        guideline_file_by_module["CORE"] = guidelines_dir / "CORE.md"

        self.tools = ToolRegistry()
        self.tools.register(VisualizeReadMeTool(
            available_modules=available_modules,
            guideline_file_by_module=guideline_file_by_module,
        ))
        self.tools.register(ShowWidgetTool(
            available_modules=available_modules,
            progressive_payloads=self._progressive_widget_payloads,
        ))

        self._skills = load_skills(agent_dir / "skills")
        self._system_prompt = build_system_prompt(self._skills)

    # -- Session delegation (keeps main.py interface unchanged) --

    def ensure_session(self, session_id: str | None) -> ChatSession:
        return self.sessions.ensure(session_id)

    def append_message(self, session: ChatSession, message: ChatMessage) -> None:
        self.sessions.append_message(session, message)

    def get_session(self, session_id: str) -> ChatSession | None:
        return self.sessions.get(session_id)

    def list_session_summaries(self) -> list[dict[str, Any]]:
        return self.sessions.list_summaries()

    # -- Agent entry point --

    def stream_reply(
        self,
        session: ChatSession,
        user_text: str,
    ) -> Generator[dict[str, Any], None, str]:
        config = resolve_config()
        logger.info(
            "stream_reply start session_id=%s key_source=%s key_present=%s user_text=%s",
            session.id, config.key_source, config.has_key, user_text,
        )
        if not config.has_key:
            logger.warning("fallback active: no GEMINI_API_KEY/GOOGLE_API_KEY found")
            return (yield from self._stream_fallback(user_text))

        logger.info("provider mode active model=%s", config.model)
        messages = self._build_messages(session, user_text)
        orchestrator = GenerativeUIOrchestrator()
        loop = AgentLoop(
            config=config, tool_registry=self.tools, orchestrator=orchestrator,
        )
        return (yield from loop.stream(messages, user_text))

    # -- Private helpers --

    def _build_messages(self, session: ChatSession, user_text: str) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": self._system_prompt}
        ]
        for msg in session.messages:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": user_text})
        return messages

    def _stream_fallback(self, user_text: str) -> Generator[dict[str, Any], None, str]:
        collected: list[str] = []
        orch = GenerativeUIOrchestrator()
        orch.on_turn_start(user_text)
        include_widget = orch.state.visual_request

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
                "loading_messages": orch._default_loading_messages(user_text),
            }
            for partial in self._progressive_widget_payloads(widget_code):
                yield {"type": "toolcall_delta", "tool_call_id": tool_call_id, "widget_code": partial}
                time.sleep(0.03)
            yield {"type": "toolcall_end", "tool_call_id": tool_call_id, "widget_code": widget_code}
        return "".join(collected)

    @staticmethod
    def _infer_widget_type(user_text: str) -> Literal["interactive", "chart", "mockup", "art", "diagram"]:
        normalized = user_text.lower()
        if any(t in normalized for t in ["chart", "graph", "plot", "histogram", "timeseries"]):
            return "chart"
        if any(t in normalized for t in ["diagram", "architecture", "flow", "workflow"]):
            return "diagram"
        if any(t in normalized for t in ["mockup", "form", "layout", "ui"]):
            return "mockup"
        if any(t in normalized for t in ["art", "illustration", "draw", "creative"]):
            return "art"
        return "interactive"

    @staticmethod
    def _simulate_text_intro(user_text: str, include_widget: bool) -> Generator[str, None, None]:
        if include_widget:
            reply = (
                f"我将为\u201c{user_text}\u201d生成一个可交互可视化。"
                "你会先看到说明文本流，然后看到 show_widget 的增量渲染事件。"
            )
        else:
            reply = (
                f"已收到你的消息：\u201c{user_text}\u201d。"
                "当前是文本流模式，你可以输入与可视化相关的问题触发工具事件流。"
            )
        for token in reply:
            yield token
            time.sleep(0.01)

    @staticmethod
    def _build_widget_html() -> str:
        return """<style>
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
</script>""".strip()

    @staticmethod
    def _progressive_widget_payloads(code: str, steps: int = 9) -> Iterable[str]:
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
