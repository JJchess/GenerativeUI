"""HTTP API for GenUI backend with session and SSE streaming chat."""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Generator, Iterable, List, Literal, Optional

from flask import Flask, Response, jsonify, request, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@dataclass
class ChatMessage:
    id: str
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: str


@dataclass
class ChatSession:
    id: str
    messages: List[ChatMessage] = field(default_factory=list)


SESSIONS: Dict[str, ChatSession] = {}


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def _ensure_session(session_id: Optional[str]) -> ChatSession:
    if session_id and session_id in SESSIONS:
        return SESSIONS[session_id]
    created = ChatSession(id=session_id or str(uuid.uuid4()))
    SESSIONS[created.id] = created
    return created


def _simulate_assistant_stream(user_text: str) -> Generator[str, None, None]:
    reply = (
        f"已收到你的消息：“{user_text}”。"
        "Phase1 流式链路已打通：后端会话已建立，前端可以实时接收增量 token。"
        "下一步会在这个流协议上接入 tool call 与 widget 渲染事件。"
    )
    for token in reply:
        yield token
        time.sleep(0.012)


def _should_stream_widget(user_text: str) -> bool:
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


def _infer_widget_type(user_text: str) -> Literal["interactive", "chart", "mockup", "art", "diagram"]:
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


def _simulate_text_intro(user_text: str, include_widget: bool) -> Generator[str, None, None]:
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


def _build_widget_html() -> str:
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


def _progressive_widget_payloads(code: str, steps: int = 9) -> Iterable[str]:
    if not code:
        return []
    fragments: List[str] = []
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


@app.get("/")
def index():
    return jsonify({"service": "GenVisuals", "status": "ok"})


@app.get("/health")
def health():
    return jsonify({"healthy": True})


@app.post("/chat/stream")
def chat_stream():
    payload = request.get_json(silent=True) or {}
    user_text = str(payload.get("message", "")).strip()
    if not user_text:
        return jsonify({"error": "message is required"}), 400

    session = _ensure_session(payload.get("session_id"))
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        role="user",
        content=user_text,
        created_at=_now_iso(),
    )
    session.messages.append(user_msg)

    assistant_msg_id = str(uuid.uuid4())
    assistant_created_at = _now_iso()

    @stream_with_context
    def event_stream():
        yield _sse("session", {"session_id": session.id})
        yield _sse(
            "message_start",
            {"message_id": assistant_msg_id, "role": "assistant", "created_at": assistant_created_at},
        )
        include_widget = _should_stream_widget(user_text)
        chunks: List[str] = []
        for delta in _simulate_text_intro(user_text, include_widget):
            chunks.append(delta)
            yield _sse("assistant_delta", {"message_id": assistant_msg_id, "delta": delta})

        if include_widget:
            tool_call_id = str(uuid.uuid4())
            widget_code = _build_widget_html()
            widget_type = _infer_widget_type(user_text)
            yield _sse(
                "toolcall_start",
                {
                    "message_id": assistant_msg_id,
                    "tool_call_id": tool_call_id,
                    "name": "show_widget",
                    "widget_type": widget_type,
                    "title": "compound_interest_demo",
                    "width": 780,
                    "height": 520,
                },
            )
            for partial in _progressive_widget_payloads(widget_code):
                yield _sse(
                    "toolcall_delta",
                    {
                        "message_id": assistant_msg_id,
                        "tool_call_id": tool_call_id,
                        "widget_code": partial,
                    },
                )
                time.sleep(0.05)
            yield _sse(
                "toolcall_end",
                {
                    "message_id": assistant_msg_id,
                    "tool_call_id": tool_call_id,
                    "widget_code": widget_code,
                },
            )
            tail = "可视化已渲染完成。你可以继续输入具体主题，我会继续用相同协议返回工具事件。"
            for delta in tail:
                chunks.append(delta)
                yield _sse("assistant_delta", {"message_id": assistant_msg_id, "delta": delta})
                time.sleep(0.01)

        assistant_content = "".join(chunks)
        session.messages.append(
            ChatMessage(
                id=assistant_msg_id,
                role="assistant",
                content=assistant_content,
                created_at=assistant_created_at,
            )
        )
        yield _sse(
            "message_end",
            {"message_id": assistant_msg_id, "session_id": session.id},
        )

    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False, threaded=True)
