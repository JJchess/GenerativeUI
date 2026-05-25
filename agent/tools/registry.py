from __future__ import annotations

from typing import Any

from agent.tools.base import AgentTool, ToolExecutionResult


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, AgentTool] = {}

    def register(self, tool: AgentTool) -> None:
        self._tools[tool.name] = tool

    def get_definitions(self) -> list[dict[str, Any]]:
        return [tool.to_definition() for tool in self._tools.values()]

    def execute(
        self,
        name: str,
        arguments: dict[str, Any],
        tool_call_id: str,
        *,
        attach_read_me_trailer: bool | None = None,
    ) -> ToolExecutionResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolExecutionResult(content=f"Tool call ignored: unknown tool name '{name}'.")
        return tool.execute(arguments, tool_call_id)
