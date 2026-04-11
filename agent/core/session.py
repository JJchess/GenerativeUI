"""Session management: CRUD and disk persistence."""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

logger = logging.getLogger("genui.session")


@dataclass
class ChatMessage:
    id: str
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: str
    blocks: list[dict[str, Any]] | None = None


@dataclass
class ChatSession:
    id: str
    messages: list[ChatMessage] = field(default_factory=list)


class SessionStore:
    def __init__(self, sessions_dir: Path) -> None:
        self.sessions_dir = sessions_dir
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, ChatSession] = {}

    def ensure(self, session_id: str | None) -> ChatSession:
        if session_id and session_id in self._cache:
            return self._cache[session_id]
        if session_id:
            loaded = self._load(session_id)
            if loaded is not None:
                self._cache[loaded.id] = loaded
                return loaded
        created = ChatSession(id=session_id or _generate_session_id())
        self._cache[created.id] = created
        self._persist(created)
        return created

    def append_message(self, session: ChatSession, message: ChatMessage) -> None:
        session.messages.append(message)
        self._persist(session)

    def get(self, session_id: str) -> ChatSession | None:
        if session_id in self._cache:
            return self._cache[session_id]
        loaded = self._load(session_id)
        if loaded is None:
            return None
        self._cache[loaded.id] = loaded
        return loaded

    def list_summaries(self) -> list[dict[str, Any]]:
        sessions_by_id: dict[str, ChatSession] = dict(self._cache)
        for file_path in sorted(
            self.sessions_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        ):
            sid = file_path.stem
            if sid in sessions_by_id:
                continue
            loaded = self._load(sid)
            if loaded is not None:
                sessions_by_id[sid] = loaded

        summaries: list[dict[str, Any]] = []
        for session in sessions_by_id.values():
            if session.messages:
                last = session.messages[-1]
                updated_at = last.created_at
                preview = last.content[:80]
            else:
                updated_at = ""
                preview = ""
            summaries.append({
                "session_id": session.id,
                "message_count": len(session.messages),
                "updated_at": updated_at,
                "preview": preview,
            })
        summaries.sort(key=lambda s: s.get("updated_at", ""), reverse=True)
        return summaries

    def _find_file(self, session_id: str) -> Path | None:
        exact = self.sessions_dir / f"{session_id}.json"
        if exact.exists():
            return exact
        for candidate in self.sessions_dir.glob(f"*_{session_id}.json"):
            return candidate
        return None

    def _load(self, session_id: str) -> ChatSession | None:
        file_path = self._find_file(session_id)
        if file_path is None:
            return None
        try:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
            messages: list[ChatMessage] = []
            for item in payload.get("messages", []):
                if not isinstance(item, dict):
                    continue
                role = str(item.get("role", "user"))
                if role not in ("user", "assistant", "system"):
                    continue
                raw_blocks = item.get("blocks")
                blocks = raw_blocks if isinstance(raw_blocks, list) else None
                messages.append(ChatMessage(
                    id=str(item.get("id", str(uuid.uuid4()))),
                    role=role,
                    content=str(item.get("content", "")),
                    created_at=str(item.get("created_at", "")),
                    blocks=blocks,
                ))
            return ChatSession(id=session_id, messages=messages)
        except Exception as exc:
            logger.error("failed to load session file %s: %s", file_path, exc)
            return None

    def _persist(self, session: ChatSession) -> None:
        payload = {
            "session_id": session.id,
            "messages": [
                {
                    "id": m.id, "role": m.role, "content": m.content,
                    "created_at": m.created_at,
                    **({"blocks": m.blocks} if m.blocks else {}),
                }
                for m in session.messages
            ],
        }
        file_path = self.sessions_dir / f"{session.id}.json"
        try:
            file_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception as exc:
            logger.error("failed to persist session %s: %s", session.id, exc)


def _generate_session_id() -> str:
    ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    return f"{ts}_{uuid.uuid4()}"
