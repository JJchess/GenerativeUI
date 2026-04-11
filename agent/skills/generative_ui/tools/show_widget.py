"""Tool: render an HTML/SVG widget in chat."""

from __future__ import annotations

import re
from typing import Any, Callable, Iterable

from agent.tools.base import AgentTool, ToolExecutionResult


class ShowWidgetTool(AgentTool):
    name = "show_widget"
    description = "Render an HTML/SVG widget in chat."

    def __init__(
        self,
        available_modules: list[str],
        progressive_payloads: Callable[[str], Iterable[str]],
    ) -> None:
        self.available_modules = available_modules
        self.progressive_payloads = progressive_payloads
        self.parameters = {
            "type": "object",
            "properties": {
                "i_have_seen_read_me": {"type": "boolean"},
                "widget_type": {"type": "string", "enum": self.available_modules},
                "title": {"type": "string"},
                "loading_messages": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 4,
                },
                "widget_code": {"type": "string"},
                "width": {"type": "number"},
                "height": {"type": "number"},
            },
            "required": ["i_have_seen_read_me", "widget_type", "title", "widget_code"],
        }

    def execute(self, arguments: dict[str, Any], tool_call_id: str) -> ToolExecutionResult:
        if not bool(arguments.get("i_have_seen_read_me")):
            return ToolExecutionResult(content="READ_ME_REQUIRED", events=[])
        title = self._normalize_title(str(arguments.get("title", "generated_widget")))
        widget_code = str(arguments.get("widget_code", "")).strip()
        widget_type_raw = str(arguments.get("widget_type", "interactive"))
        widget_type = widget_type_raw if widget_type_raw in self.available_modules else "interactive"
        loading_messages = self._safe_loading_messages(arguments.get("loading_messages"))
        width = self._safe_int(arguments.get("width"), 780)
        height = self._safe_int(arguments.get("height"), 520)
        if not self._is_widget_code_valid(widget_code):
            return ToolExecutionResult(content="INVALID_WIDGET_CODE", events=[])

        events: list[dict[str, Any]] = [
            {
                "type": "toolcall_start",
                "tool_call_id": tool_call_id,
                "name": "show_widget",
                "widget_type": widget_type,
                "title": title,
                "width": width,
                "height": height,
                "loading_messages": loading_messages,
            }
        ]
        for partial in self.progressive_payloads(widget_code):
            events.append({"type": "toolcall_delta", "tool_call_id": tool_call_id, "widget_code": partial})
        events.append({"type": "toolcall_end", "tool_call_id": tool_call_id, "widget_code": widget_code})
        return ToolExecutionResult(content=f'Widget "{title}" rendered ({width}x{height}).', events=events)

    def _safe_int(self, value: Any, default: int) -> int:
        try:
            return int(value)
        except Exception:
            return default

    def _normalize_title(self, title: str) -> str:
        normalized = re.sub(r"[^a-zA-Z0-9_]+", "_", title.strip().lower())
        normalized = re.sub(r"_+", "_", normalized).strip("_")
        return normalized or "generated_widget"

    def _safe_loading_messages(self, raw: Any) -> list[str]:
        if not isinstance(raw, list):
            return ["Preparing visual layout", "Rendering interactive widget"]
        values = [str(item).strip() for item in raw if str(item).strip()]
        if not values:
            return ["Preparing visual layout", "Rendering interactive widget"]
        return values[:4]

    def _is_widget_code_valid(self, widget_code: str) -> bool:
        normalized = widget_code.lower()
        if len(widget_code) < 120:
            return False
        if any(tag in normalized for tag in ("<!doctype", "<html", "<head", "<body")):
            return False
        has_ui_root = any(token in normalized for token in ("<div", "<svg", "<canvas"))
        has_interaction = any(token in normalized for token in ("<button", "addEventListener", "onclick", "oninput"))
        has_script = "<script" in normalized
        if not (has_ui_root and has_interaction and has_script):
            return False
        first_ui_root_idx = min(
            i for i in (normalized.find("<div"), normalized.find("<svg"), normalized.find("<canvas")) if i >= 0
        )
        script_idx = normalized.find("<script")
        if script_idx < first_ui_root_idx:
            return False
        style_idx = normalized.find("<style")
        if style_idx >= 0 and script_idx < style_idx:
            return False
        return True
