---
name: generative_ui
description: Generate self-contained visual widgets for charts, diagrams, mockups, and simulations.
always: true
---

## When to use

- Use `generative_ui` when the user is asking for a chart, diagram, interactive explainer, simulation, mockup, or other visual widget.
- Pass the user's request in `query`.
- Prefer this tool over writing raw HTML, SVG, or widget JSON directly in the assistant reply.

## Tool rules

- The tool returns widget metadata plus a renderable HTML fragment.
- After the tool succeeds, continue with a short plain-text response only.
- Do not manually fabricate tool output in normal assistant text.
- Keep visible text in the same language as the user's request.
