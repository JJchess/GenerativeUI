"""Tool: load design guidelines for visualization modules."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agent.tools.base import AgentTool, ToolExecutionResult

# Appended to successful payloads: parameter shape + structural few-shot (not duplicated in SKILL).
_READ_ME_OUTPUT_TRAILER = """

---
## Required next action

Call show_widget now with i_have_seen_read_me=true and a complete widget_code fragment.

## show_widget arguments shape
```json
{
  "i_have_seen_read_me": true,
  "title": "descriptive_name",
  "widget_type": "interactive",
  "width": 780,
  "height": 520,
  "loading_messages": ["Step one", "Step two"],
  "widget_code": "<style>:root{--bg:#0f1117;--accent:#4fc3f7}</style><canvas id='c'></canvas><script>...</script>"
}
```

## widget_code structural example (NaCl electrolysis)
<style>
  :root { --bg: #0f1117; --accent: #4fc3f7; --text: #e0e0e0; }
  body { margin: 0; background: var(--bg); }
  canvas { display: block; margin: 0 auto; }
  #controls { text-align: center; margin-top: 8px; }
  button { background: var(--accent); color: #000; border: none;
           padding: 6px 18px; border-radius: 4px; cursor: pointer; }
</style>
<canvas id="c" width="740" height="440"></canvas>
<div id="controls"><button id="btn">Start</button></div>
<script>
  const canvas = document.getElementById('c');
  const ctx = canvas.getContext('2d');
  let running = false;
  document.getElementById('btn').onclick = () => { running = !running; };
  function draw(t) {
    ctx.clearRect(0, 0, 740, 440);
    // draw electrodes, ions, bubbles here
    if (running) requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);
</script>
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
