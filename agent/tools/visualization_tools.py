from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

from agent.tools.base import AgentTool, ToolExecutionResult


class VisualizeReadMeTool(AgentTool):
    name = "visualize_read_me"
    description = "Load design guidelines for one or more visualization modules."

    def __init__(self, available_modules: list[str], guideline_file_by_module: dict[str, Path]) -> None:
        self.available_modules = available_modules
        self.guideline_file_by_module = guideline_file_by_module
        self.parameters = {
            "type": "object",
            "properties": {
                "modules": {
                    "type": "array",
                    "items": {"type": "string", "enum": self.available_modules},
                }
            },
            "required": ["modules"],
        }

    def execute(self, arguments: dict[str, Any], tool_call_id: str) -> ToolExecutionResult:
        modules = arguments.get("modules")
        modules_list = [m for m in modules if isinstance(m, str)] if isinstance(modules, list) else []
        modules_list = [m for m in modules_list if m in self.available_modules]
        chunks: list[str] = []
        for module in modules_list:
            path = self.guideline_file_by_module.get(module)
            if not path or not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            chunks.append(f"<module name=\"{module}\">\n{text}\n</module>")
        if not chunks:
            return ToolExecutionResult(content="No guidelines found for requested modules.")
        return ToolExecutionResult(content="\n\n".join(chunks))


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
                "widget_type": {"type": "string", "enum": self.available_modules},
                "title": {"type": "string"},
                "widget_code": {"type": "string"},
                "width": {"type": "number"},
                "height": {"type": "number"},
            },
            "required": ["widget_type", "title", "widget_code"],
        }

    def execute(self, arguments: dict[str, Any], tool_call_id: str) -> ToolExecutionResult:
        title = str(arguments.get("title", "generated_widget"))
        widget_code = str(arguments.get("widget_code", "")).strip()
        widget_type_raw = str(arguments.get("widget_type", "interactive"))
        widget_type = widget_type_raw if widget_type_raw in self.available_modules else "interactive"
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

    def _is_widget_code_valid(self, widget_code: str) -> bool:
        normalized = widget_code.lower()
        if len(widget_code) < 120:
            return False
        has_ui_root = any(token in normalized for token in ("<div", "<svg", "<canvas"))
        has_interaction = any(token in normalized for token in ("<button", "addEventListener", "onclick", "oninput"))
        has_script = "<script" in normalized
        return has_ui_root and has_interaction and has_script
