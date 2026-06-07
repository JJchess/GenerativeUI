"""Tool: load design guidelines for visualization modules."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agent.skills.generative_ui.prompts import EXAMPLE_WIDGET_CODE
from agent.tools.base import AgentTool, ToolExecutionResult

# Appended to successful payloads: parameter shape + structural few-shot (not duplicated in SKILL).
_READ_ME_OUTPUT_TRAILER = f"""

---
## Required next action

Call show_widget now with i_have_seen_read_me=true and a complete widget_code fragment.

## show_widget arguments shape
```json
{{
  "i_have_seen_read_me": true,
  "title": "descriptive_name",
  "widget_type": "interactive",
  "width": 780,
  "height": 520,
  "loading_messages": ["Step one", "Step two"],
  "widget_code": "<style>.lab{{background:#0D1322;border-radius:16px;padding:20px}}</style><div class='lab'>...</div><script>...</script>"
}}
```

## widget_code structural example (damped pendulum, aesthetic direction: lab-dark)
The direction is committed fully — self-contained panel, gridline + glow signature, mono tabular readout, restyled controls with hover/active states. Commit to YOUR chosen direction just as completely; a different subject mood means different colors, type, and motion (see the direction library in the guidelines).

{EXAMPLE_WIDGET_CODE}
"""


class VisualizeReadMeTool(AgentTool):
    name = "visualize_read_me"
    description = (
        "Load exactly one guideline file per call (full text, never truncated by the host). "
        "Pass a single-element `modules` array naming the module (e.g. interactive). "
        "Use module CORE only when no other listed module type fits the user task; do not combine multiple modules in one call—call again for another file if needed."
    )

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
                    "minItems": 1,
                    "maxItems": 1,
                    "items": {"type": "string", "enum": self.available_modules},
                }
            },
            "required": ["modules"],
        }

    def execute(
        self,
        arguments: dict[str, Any],
        tool_call_id: str,
        *,
        attach_output_trailer: bool = True,
    ) -> ToolExecutionResult:
        modules = arguments.get("modules")
        modules_list = [m for m in modules if isinstance(m, str)] if isinstance(modules, list) else []
        modules_list = [m for m in modules_list if m in self.available_modules][:1]
        chunks: list[str] = []
        for module in modules_list:
            path = self.guideline_file_by_module.get(module)
            if not path or not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            chunks.append(f'<module name="{module}">\n{text}\n</module>')
        if not chunks:
            return ToolExecutionResult(content="No guidelines found for requested modules.")
        body = "\n\n".join(chunks)
        suffix = _READ_ME_OUTPUT_TRAILER if attach_output_trailer else ""
        return ToolExecutionResult(content=body + suffix)
