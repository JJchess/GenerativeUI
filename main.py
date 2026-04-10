"""HTTP API for GenUI backend with session and SSE streaming chat."""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Generator, List, Literal, Optional

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
        chunks: List[str] = []
        for delta in _simulate_assistant_stream(user_text):
            chunks.append(delta)
            yield _sse("assistant_delta", {"message_id": assistant_msg_id, "delta": delta})

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
