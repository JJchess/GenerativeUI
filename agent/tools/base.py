from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolExecutionResult:
    content: str
    events: list[dict[str, Any]] = field(default_factory=list)


class AgentTool(ABC):
    name: str
    description: str
    parameters: dict[str, Any]

    def to_definition(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    @abstractmethod
    def execute(self, arguments: dict[str, Any], tool_call_id: str) -> ToolExecutionResult:
        raise NotImplementedError
