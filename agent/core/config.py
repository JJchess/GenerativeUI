"""Agent configuration: API key resolution, model settings."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger("genui.config")


@dataclass(frozen=True)
class AgentConfig:
    api_key: str
    key_source: str
    model: str

    @property
    def has_key(self) -> bool:
        return bool(self.api_key)


def resolve_config() -> AgentConfig:
    api_key, key_source = _resolve_api_key()
    model = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
    return AgentConfig(api_key=api_key, key_source=key_source, model=model)


def _resolve_api_key() -> tuple[str, str]:
    for key_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        value = os.getenv(key_name, "").strip()
        if value:
            return value, key_name
    dotenv_values = _read_backend_dotenv()
    for key_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        value = dotenv_values.get(key_name, "").strip()
        if value:
            return value, f".env:{key_name}"
    return "", "none"


def _read_backend_dotenv() -> dict[str, str]:
    dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
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
