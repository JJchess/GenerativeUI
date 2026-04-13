---
name: generative_ui
description: Route visualization requests to read_me and show_widget tools.
always: true
---

## Visualization rules

**Tool order (mandatory):**

1. Call `visualize_read_me` first — pass **`modules` with exactly one string** (one guideline file per call). Pick the best-matching module from the hints below. Use **`CORE`** only when none of the specialized modules fit; never bundle multiple modules in a single `visualize_read_me` call (call again for another file if needed).
2. After receiving the tool result, call `show_widget` with `i_have_seen_read_me: true` and a `widget_type` from the specialized list (not `CORE`).
3. After `show_widget` succeeds, reply with plain text explanation only. Do not call tools again.

**Module hints (specialized — prefer these over CORE):**

- Animation / interaction → `interactive`
- Charts / data → `chart` or `chart_interactive`
- Flow / structure → `diagram`
- Artistic interactive → `art_interactive`

**widget_code rules:**

- Fragment only — no `<!doctype>`, `<html>`, `<head>`, `<body>`
- Order: `<style>` → markup → `<script>`
- Use CSS variables for all colors (defined in `--bg`, `--accent`, etc.)
- All explanations go in assistant text, not inside `widget_code`
