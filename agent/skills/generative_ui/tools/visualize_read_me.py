"""Tool: load design guidelines for visualization modules."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agent.tools.base import AgentTool, ToolExecutionResult


class VisualizeReadMeTool(AgentTool):
    name = "visualize_read_me"
    description = "Load design guidelines for one or more visualization modules."

    def __init__(
        self,
        available_modules: list[str],
        guideline_file_by_module: dict[str, Path],
    ) -> None:
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
            chunks.append(f'<module name="{module}">\n{text}\n</module>')
        if not chunks:
            return ToolExecutionResult(content="No guidelines found for requested modules.")
        return ToolExecutionResult(content="\n\n".join(chunks))
