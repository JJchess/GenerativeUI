from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

from .constants import CORE_GUIDANCE, MODULE_GUIDANCE


def recent_conversation_context(history: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for msg in history[-6:]:
        if not isinstance(msg, dict):
            continue
        role = str(msg.get("role") or "unknown")
        name = str(msg.get("character_name") or msg.get("role_id") or "").strip()
        content = str(msg.get("content") or "").strip()
        if not content:
            continue
        prefix = f"{role}:{name}" if name else role
        lines.append(f"{prefix}: {content[:300]}")
    return "\n".join(lines) if lines else "(none)"


_GUIDELINES_DIR = Path(__file__).resolve().parents[2] / "guidelines"


@lru_cache(maxsize=None)
def _read_guideline_file(name: str) -> str:
    path = _GUIDELINES_DIR / f"{name}.md"
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def _guideline_bundle(widget_type: str) -> str:
    parts: List[str] = []

    core = _read_guideline_file("CORE")
    if core:
        parts.append(f'<module name="CORE">\n{core}\n</module>')
    else:
        parts.append(f'<module name="CORE">\n{CORE_GUIDANCE}\n</module>')

    module = _read_guideline_file(widget_type)
    if module:
        parts.append(f'<module name="{widget_type}">\n{module}\n</module>')
    else:
        fallback = MODULE_GUIDANCE.get(widget_type, MODULE_GUIDANCE["interactive"])
        parts.append(f'<module name="{widget_type}">\n{fallback}\n</module>')

    return "\n\n".join(parts)


_STRUCTURAL_EXAMPLE = """
## Structural example (NaCl electrolysis)

{"title": "nacl_electrolysis", "widget_type": "interactive", "loading_messages": ["Preparing simulation", "Rendering ions"], "assistant_text": "An interactive NaCl electrolysis simulation with start/stop control."}
<widget_code>
<style>
  .wrap { width: 100%; }
  canvas { display: block; width: 100%; max-width: 740px; height: auto; margin: 0 auto;
           background: var(--color-background-secondary); border-radius: var(--border-radius-md); }
  #controls { text-align: center; margin-top: 8px; }
</style>
<div class="wrap">
  <canvas id="c" width="740" height="440"></canvas>
  <div id="controls"><button id="btn">Start</button></div>
</div>
<script>
  const canvas = document.getElementById('c');
  const ctx = canvas.getContext('2d');
  let running = false;
  document.getElementById('btn').addEventListener('click', () => {
    running = !running;
    document.getElementById('btn').textContent = running ? 'Stop' : 'Start';
    if (running) requestAnimationFrame(draw);
  });
  let t = 0;
  function draw() {
    ctx.clearRect(0, 0, 740, 440);
    ctx.fillStyle = '#4fc3f7';
    ctx.fillRect(60, 80, 20, 280);
    ctx.fillRect(660, 80, 20, 280);
    t += 0.05;
    for (let i = 0; i < 20; i++) {
      const x = 100 + (i % 10) * 54 + Math.sin(t + i) * 10;
      const y = 150 + Math.floor(i / 10) * 120 + Math.cos(t + i * 0.7) * 15;
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, Math.PI * 2);
      ctx.fillStyle = i % 2 === 0 ? '#ef5350' : '#42a5f5';
      ctx.fill();
      ctx.fillStyle = '#fff';
      ctx.font = '9px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(i % 2 === 0 ? 'Na+' : 'Cl-', x, y);
    }
    if (running) requestAnimationFrame(draw);
  }
  draw();
</script>
</widget_code>
""".strip()


def build_planning_prompt(
    *,
    query: str,
    widget_type: str,
    recent_context: str,
) -> str:
    return f"""
You are the design-planning step for an interactive UI widget generator. You do NOT write final HTML/CSS/JS here. You produce a STRUCTURAL CONTRACT as JSON — a precise blueprint that the next step implements verbatim. The contract pins down the three things that most often go wrong (layout, state, interaction) while leaving styling and drawing details to the implementer.

Current request:
{query}

Suggested widget type:
{widget_type}

Relevant recent conversation:
{recent_context}

Think about what makes this a GOOD demonstration — not a static picture. For conceptual/technical topics (algorithms, architectures, physical systems, math), the user wants to manipulate something and SEE the consequence. A static labelled diagram with a click-to-show-text panel is a failure mode — avoid it.

CLARITY BEATS RICHNESS. The single most important thing is that the core concept reads crisply and unambiguously. A clean diagram that shows ONE idea sharply is far better than a busy widget with many controls where the main visual is muddy. Do NOT add extra controls, modes, or parameters (extra kernels, free-form editing, multiple toggles) if they make the central visualization harder to read. When in doubt, cut.

Rendering medium — choose deliberately, state it in the contract:
- Geometric / structural concepts (boundaries, lines, vectors, regions, graphs, flows, hierarchies) → DECLARATIVE SVG with named elements (`<line>`, `<path>`, `<circle>`). Crisp vector strokes. Compute lines/curves ANALYTICALLY and set element coordinates — NEVER draw a boundary by sampling a pixel grid and dotting cells; that looks blurry and noisy.
- Use `<canvas>` ONLY for genuinely pixel/particle-heavy content: many moving particles, continuous fields, fluid/heat simulation, dense per-pixel shading. If the core visual is lines and shapes, canvas is the wrong tool.
- Note: canvas does NOT reliably resolve `var(--color-*)` for fillStyle/strokeStyle — another reason to prefer SVG for anything color-coded.

Design rules the contract MUST respect:
- Width is fluid (host-driven, unknown). Layout uses 100% / 1fr / minmax(0,1fr) — never fixed pixel widths on regions. Height grows with content.
- At least one control must produce a VISIBLE change in the main visualization.
- The initial render is non-empty and meaningful — never "click to start".
- There is ONE update entry point: every state change calls a single update() that re-derives the view from current state. For SVG this means updating the named elements' attributes; for canvas it means a redraw. Either way, no scattered ad-hoc mutations spread across handlers.

Return ONE JSON object only — no prose, no markdown fences. Schema:

{{
  "core_insight": "<one sentence — what the user should understand after using this>",
  "render_medium": "svg | canvas",
  "render_medium_reason": "<short — why this medium fits the core visual>",
  "layout_skeleton": "<region tree, top-to-bottom, with the fluid sizing for each region, e.g. 'controls bar (100%) / main svg viz (100%, aspect-ratio kept) / readout row (2x 1fr)'>",
  "state_model": [
    {{"name": "<jsVarName>", "type": "int|float|bool|string|array", "range_or_values": "<e.g. 0..7, true/false, ['我','爱','你']>", "initial": "<concrete initial value>"}}
  ],
  "interactions": [
    {{"trigger": "<element + event, e.g. 'range#heads input'>", "effect": "<which state changes and what updates visually>"}}
  ],
  "render_contract": "<one sentence: what update() re-derives from state, and (for SVG) which named elements it sets, or (for canvas) what it redraws>",
  "initial_paint": "<what is on screen at first render, with concrete values from state_model initials>"
}}

Keep every string tight and concrete. Prefer \"range#k (1..8) -> recompute neighbors, recolor decision regions\" over \"interactive slider\". The state_model names you choose ARE the variable names the implementer will use.
""".strip()


def build_primary_prompt(
    *,
    query: str,
    widget_type: str,
    recent_context: str,
    plan: str = "",
) -> str:
    plan_section = (
        "\nStructural contract to implement (from the planning step — implement it faithfully, "
        "do not redesign). Use the exact state_model variable names, wire every interaction's "
        "trigger to a real event handler, and route all updates through the single update() the "
        "render_contract describes. Honor render_medium: if it says svg, build the visual from "
        "named SVG elements and compute lines/curves analytically (never sample a pixel grid to "
        "draw a boundary); if it says canvas, reserve it for particle/field-style content. "
        "Keep the core visual crisp — prefer clarity over extra controls:\n"
        f"{plan}\n"
        if plan.strip()
        else ""
    )
    return f"""
You are generating a self-contained interactive UI widget for the current discussion.

Write ALL user-facing text (title, loading_messages, assistant_text, visible widget strings) in the SAME language as the current request. Code identifiers and JSON keys stay ASCII.

Current request:
{query}

Suggested widget type:
{widget_type}

Relevant recent conversation:
{recent_context}
{plan_section}
Visualization skill guidance:
{_guideline_bundle(widget_type)}

{_STRUCTURAL_EXAMPLE}

---

Your response MUST have exactly two parts in this order - nothing else:

Part 1 - a single JSON object on one or more lines (no widget_code field):
{{
  "title": "<short title, SAME language as the request>",
  "widget_type": "{widget_type}",
  "loading_messages": ["<msg in request's language>", "..."],
  "assistant_text": "<one short sentence in the request's language>"
}}

Part 2 - the widget HTML/CSS/JS wrapped in <widget_code> tags (raw, NOT JSON-escaped):
<widget_code>
<style>...</style>
<div>...</div>
<script>...</script>
</widget_code>

Rules:
- widget_type must stay "{widget_type}" unless the request clearly requires another allowed type.
- assistant_text must be one short natural sentence only.
- widget_code must be a complete self-contained HTML fragment ready to render in a sandboxed iframe.
- No <!doctype>, <html>, <head>, <body> tags.
- Structure order inside widget_code: <style> first, then markup, then <script>.
- Do NOT JSON-escape widget_code - write it as raw HTML/CSS/JS between the tags.
- Use the current request as the primary goal; use recent conversation only when it sharpens the intended UI.
- Put explanations in assistant_text, not inside the widget body.
- No markdown fences around the JSON.
- No text outside these two parts.

Layout — width is fluid, height is content-driven (THIS IS LOAD-BEARING, READ CAREFULLY):
- The host container has a fixed width that you do NOT know. Design the widget to be FLUID horizontally.
- NEVER hardcode pixel widths on layout containers. Forbidden patterns: `width: 800px`, `width: 600px`, `min-width: 700px`, `grid-template-columns: 180px 1fr 240px` (fixed pixel tracks force overflow on narrow hosts).
- Use `width: 100%`, `max-width: <Npx>`, fractional units (`1fr`), or `minmax(0, 1fr)` for grid tracks. For multi-column layouts prefer `grid-template-columns: repeat(auto-fit, minmax(<Npx>, 1fr))` or all-`1fr` tracks.
- Canvas and images have intrinsic pixel dimensions for drawing — that is fine on the element itself, but ALWAYS wrap them with `style="width:100%; max-width:<Npx>; height:auto; display:block"` so they shrink with the host.
- Height: do NOT set a fixed pixel height on any outer/root wrapper. The frame grows to fit your content. Inner regions (a heatmap cell, a canvas) may have pixel heights, but the root container must let height be `auto`.
- Do NOT use `overflow: hidden` on the outermost wrapper — it hides content when your size guess is wrong.
- Verify mentally: would your widget still look right if the host were 600px wide? 900px wide? If not, redesign with fluid units.
""".strip()


def build_repair_prompt(*, query: str, broken_payload: Dict[str, Any]) -> str:
    import json as _json

    widget_type = str(broken_payload.get("widget_type") or "interactive")
    display_payload = {k: v for k, v in broken_payload.items() if k != "widget_code"}
    widget_code_snippet = str(broken_payload.get("widget_code") or "")[:300]
    return f"""
Fix the following widget response so it is valid and renderable.

Write ALL user-facing text (title, loading_messages, assistant_text, visible widget strings) in the SAME language as the original request. Code identifiers and JSON keys stay ASCII.

Original request:
{query}

Broken metadata (widget_code excluded):
{_json.dumps(display_payload, ensure_ascii=False)}

Broken widget_code (first 300 chars):
{widget_code_snippet}

Relevant guidance:
{_guideline_bundle(widget_type)}

Return the fixed response in EXACTLY the same two-part format:

Part 1 - metadata JSON (no widget_code field, no width/height):
{{"title": "...", "widget_type": "{widget_type}", "loading_messages": [...], "assistant_text": "..."}}

Part 2 - raw widget HTML/CSS/JS:
<widget_code>
<style>...</style>
...markup...
<script>...</script>
</widget_code>

Validation rules for widget_code:
- Must be an HTML fragment (no <!doctype>, <html>, <head>, <body>).
- Must contain at least one of: <div>, <svg>, <canvas>, <style>.
- Length must be at least 50 characters.
- Do NOT JSON-escape the widget_code - write it raw between the tags.
""".strip()


def build_validation_repair_prompt(
    *,
    query: str,
    widget_type: str,
    recent_context: str,
    broken_payload: Dict[str, Any],
    validation_errors: List[str],
) -> str:
    import json as _json

    error_lines = "\n".join(f"- {item}" for item in validation_errors) or "- payload is invalid"
    display_payload = {k: v for k, v in broken_payload.items() if k != "widget_code"}
    widget_code_snippet = str(broken_payload.get("widget_code") or "")[:300]
    return f"""
Regenerate this widget response so it passes validation and stays faithful to the request.

Write ALL user-facing text (title, loading_messages, assistant_text, visible widget strings) in the SAME language as the current request. Code identifiers and JSON keys stay ASCII.

Current request:
{query}

Suggested widget type:
{widget_type}

Relevant recent conversation:
{recent_context}

Previous invalid metadata:
{_json.dumps(display_payload, ensure_ascii=False)}

Previous invalid widget_code (first 300 chars):
{widget_code_snippet}

Validation errors to fix:
{error_lines}

Visualization skill guidance:
{_guideline_bundle(widget_type)}

Return the fixed response in EXACTLY the same two-part format:

Part 1 - metadata JSON (no widget_code field, no width/height):
{{
  "title": "<short title, SAME language as the request>",
  "widget_type": "{widget_type}",
  "loading_messages": ["<msg in request's language>", "..."],
  "assistant_text": "<one short sentence in the request's language>"
}}

Part 2 - raw widget HTML/CSS/JS:
<widget_code>
<style>...</style>
...markup...
<script>...</script>
</widget_code>

Requirements:
- Fix every validation error listed above.
- Keep widget_type as "{widget_type}" unless the request absolutely forces another allowed type.
- Keep the widget self-contained and renderable inside a sandboxed iframe.
- Do NOT JSON-escape widget_code - write it raw between the tags.
- Put explanations in assistant_text, not inside the widget body.
""".strip()
