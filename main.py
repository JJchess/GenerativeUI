"""HTTP API for GenUI backend with session and SSE streaming chat."""

from __future__ import annotations

import json
import logging
import time
import uuid

from flask import Flask, Response, jsonify, request, stream_with_context
from flask_cors import CORS

from agent.core.session import message_public_dict
from agent.service import ChatMessage, GenUIAgentService
from logger import reset_log_session_id, set_log_session_id, setup_logger

setup_logger()
logger = logging.getLogger("genui.api")
app = Flask(__name__)
CORS(app)
agent_service = GenUIAgentService()


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.get("/")
def index():
    return jsonify({"service": "GenVisuals", "status": "ok"})


@app.get("/health")
def health():
    return jsonify({"healthy": True})


@app.get("/chat/sessions")
def list_sessions():
    return jsonify({"sessions": agent_service.list_session_summaries()})


@app.get("/chat/sessions/<session_id>")
def get_session(session_id: str):
    session = agent_service.get_session(session_id)
    if session is None:
        return jsonify({"error": "session not found"}), 404
    return jsonify(
        {
            "session_id": session.id,
            "messages": [message_public_dict(msg) for msg in session.messages],
        }
    )


@app.post("/chat/stream")
def chat_stream():
    payload = request.get_json(silent=True) or {}
    user_text = str(payload.get("message", "")).strip()
    if not user_text:
        return jsonify({"error": "message is required"}), 400
    session = agent_service.ensure_session(payload.get("session_id"))
    logger.info("chat request received len=%s", len(user_text), extra={"session_id": session.id})
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        role="user",
        content=user_text,
        created_at=_now_iso(),
    )
    agent_service.append_message(session, user_msg)

    assistant_msg_id = str(uuid.uuid4())
    assistant_created_at = _now_iso()

    @stream_with_context
    def event_stream():
        token = set_log_session_id(session.id)
        try:
            yield _sse("session", {"session_id": session.id})
            yield _sse(
                "message_start",
                {"message_id": assistant_msg_id, "role": "assistant", "created_at": assistant_created_at},
            )
            for event in agent_service.stream_reply(
                session=session,
                user_text=user_text,
                persist_assistant=(assistant_msg_id, assistant_created_at),
            ):
                event_type = event.get("type")
                if event_type == "assistant_delta":
                    delta = str(event.get("delta", ""))
                    yield _sse("assistant_delta", {"message_id": assistant_msg_id, "delta": delta})
                    continue
                if event_type == "toolcall_start":
                    tcid = event.get("tool_call_id")
                    yield _sse(
                        "toolcall_start",
                        {
                            "message_id": assistant_msg_id,
                            "tool_call_id": tcid,
                            "name": event.get("name"),
                            "widget_type": event.get("widget_type"),
                            "title": event.get("title"),
                            "width": event.get("width"),
                            "height": event.get("height"),
                            "loading_messages": event.get("loading_messages"),
                        },
                    )
                    continue
                if event_type == "toolcall_delta":
                    yield _sse(
                        "toolcall_delta",
                        {
                            "message_id": assistant_msg_id,
                            "tool_call_id": event.get("tool_call_id"),
                            "widget_code": event.get("widget_code", ""),
                        },
                    )
                    continue
                if event_type == "toolcall_end":
                    tcid = event.get("tool_call_id")
                    final_code = event.get("widget_code", "")
                    yield _sse(
                        "toolcall_end",
                        {
                            "message_id": assistant_msg_id,
                            "tool_call_id": tcid,
                            "widget_code": final_code,
                        },
                    )
                    continue
            yield _sse(
                "message_end",
                {"message_id": assistant_msg_id, "session_id": session.id},
            )
        finally:
            reset_log_session_id(token)

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
