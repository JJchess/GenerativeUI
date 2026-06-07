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
    # Each module file is self-contained — it already embeds the full CORE design
    # system plus its module-specific guidance. So we load exactly ONE document by
    # need; CORE.md is only the fallback when no module matches the widget_type.
    # (Loading CORE + module together would inject the core design system twice.)
    module = _read_guideline_file(widget_type)
    if module:
        return f'<module name="{widget_type}">\n{module}\n</module>'

    core = _read_guideline_file("CORE")
    if core:
        return f'<module name="CORE">\n{core}\n</module>'

    fallback = MODULE_GUIDANCE.get(widget_type) or CORE_GUIDANCE
    return f'<module name="{widget_type}">\n{fallback}\n</module>'


# Shared high-craft example. It demonstrates a fully-committed aesthetic direction
# (lab-dark): self-contained panel, gridline + glow signature details, mono tabular
# readouts, restyled controls with hover/active states, fluid width, single update().
EXAMPLE_WIDGET_CODE = """
<style>
  .lab { background: #0D1322; border-radius: 16px; padding: 20px; color: #E2E8F0; font-family: var(--font-sans); }
  .lab canvas { display: block; width: 100%; max-width: 680px; height: auto; margin: 0 auto;
                background: linear-gradient(180deg, #0D1322, #121C32); border-radius: 12px; }
  .row { display: flex; align-items: center; gap: 12px; margin-top: 16px; }
  .lab label { font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: #94A3B8; }
  .lab input[type=range] { flex: 1; height: 4px; background: #243049; border-radius: 2px; }
  .lab input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px;
    border-radius: 50%; background: #22D3EE; box-shadow: 0 0 8px rgba(34,211,238,.6); cursor: pointer; }
  .val { font-family: ui-monospace, 'Cascadia Mono', Consolas, monospace; font-variant-numeric: tabular-nums;
         font-size: 14px; color: #22D3EE; min-width: 48px; text-align: right; }
  .lab button { background: #1B2538; color: #E2E8F0; border: 1px solid rgba(148,163,184,.25);
                border-radius: 8px; padding: 6px 18px; font-size: 14px; cursor: pointer;
                transition: background .15s, transform .1s; }
  .lab button:hover { background: #243049; }
  .lab button:active { transform: scale(.97); }
</style>
<div class="lab">
  <canvas id="stage" width="680" height="320"></canvas>
  <div class="row">
    <label for="damp">Damping</label>
    <input type="range" id="damp" min="0" max="0.2" step="0.01" value="0.05">
    <span class="val" id="dampVal">0.05</span>
    <button id="reset">Reset</button>
  </div>
</div>
<script>
  const ctx = document.getElementById('stage').getContext('2d');
  let damp = 0.05, theta = Math.PI / 3, omega = 0;
  const L = 220, ox = 340, oy = 30;
  document.getElementById('damp').addEventListener('input', (e) => {
    damp = parseFloat(e.target.value);
    document.getElementById('dampVal').textContent = damp.toFixed(2);
  });
  document.getElementById('reset').addEventListener('click', () => { theta = Math.PI / 3; omega = 0; });
  function step(dt) {
    omega += (-9.8 / 2.4 * Math.sin(theta) - damp * omega) * dt;
    theta += omega * dt;
  }
  function draw() {
    ctx.clearRect(0, 0, 680, 320);
    ctx.strokeStyle = 'rgba(148,163,184,.08)';
    ctx.lineWidth = 1;
    for (let x = 40; x < 680; x += 40) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 320); ctx.stroke(); }
    const bx = ox + L * Math.sin(theta), by = oy + L * Math.cos(theta);
    ctx.strokeStyle = '#94A3B8'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(bx, by); ctx.stroke();
    ctx.shadowColor = '#22D3EE'; ctx.shadowBlur = 14;
    ctx.fillStyle = '#22D3EE';
    ctx.beginPath(); ctx.arc(bx, by, 12, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
  }
  let last = performance.now();
  (function loop(now) {
    step(Math.min((now - last) / 1000, 0.03)); last = now;
    draw();
    requestAnimationFrame(loop);
  })(performance.now());
</script>
""".strip()


_STRUCTURAL_EXAMPLE = f"""
## Structural example (damped pendulum, aesthetic_direction: lab-dark)

Notice how the direction is committed fully — panel surface, gridline + glow signature, mono tabular readout, restyled controls with hover/active states. Your widget should commit to ITS direction just as completely, with different colors/type/motion when the subject calls for a different mood.

{{"title": "damped_pendulum_lab", "widget_type": "interactive", "loading_messages": ["Calibrating pendulum", "Lighting the lab"], "assistant_text": "An interactive damped pendulum — drag the slider to change damping."}}
<widget_code>
{EXAMPLE_WIDGET_CODE}
</widget_code>
""".strip()


def build_planning_prompt(
    *,
    query: str,
    widget_type: str,
    recent_context: str,
) -> str:
    return f"""
You are the design-planning step for an interactive UI widget generator. You do NOT write final HTML/CSS/JS here. You produce a STRUCTURAL CONTRACT as JSON — a precise blueprint that the next step implements verbatim. The contract pins down the four things that most often go wrong (layout, state, interaction, aesthetic direction) while leaving drawing details to the implementer.

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

Aesthetic direction — pick ONE deliberately (the implementation step receives the full specs; this is the menu):
- lab-dark: dark precision stage, cyan/magenta glow, mono readouts — physics/chem/algorithm sims, particles, waves
- paper-editorial: warm paper, serif display, terracotta/moss — poetry, literature, history, language, philosophy
- studio-pop: white + bold geometric color blocks, hard offset shadows — art, design, music, playful or kid-facing topics
- terminal-data: charcoal, mono tabular numerals, green/red deltas — finance, metrics, performance dashboards
- soft-organic: cream + sage/clay blob shapes, breathing motion — biology, nature, health, food, emotions
- blueprint: pale grid + indigo ink, dashed construction lines — mechanics, architecture, how-things-work cutaways
- host-calm: app-native quiet, host CSS variables — data records, forms, business UI mockups
Match the SUBJECT's mood, not habit. Variety is a goal: widgets on different topics must not share a direction. If the user names a style ("cyberpunk", "watercolor"), answer custom:<name> and define the palette yourself.

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
  "aesthetic_direction": "<lab-dark | paper-editorial | studio-pop | terminal-data | soft-organic | blueprint | host-calm | custom:<short-name>>",
  "direction_reason": "<one short clause — why this direction fits this subject>",
  "palette": ["<surface hex>", "<ink hex>", "<accent1 hex>", "<accent2 hex, optional>"],
  "signature_detail": "<ONE memorable visual idea, e.g. 'glowing bob with fading motion trail', 'oversized serif drop cap', 'dashed dimension arrows with end ticks'>",
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
        "Honor the design brief: commit fully to aesthetic_direction using its palette and the "
        "signature_detail — the skill guidance below carries the full direction specs (surface, "
        "ink, type, motion). Keep the core visual crisp — prefer clarity over extra controls:\n"
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

Before emitting, run the beauty check from the skill guidance: direction committed fully, one signature detail present, every interactive element has hover/active feedback with a transition, exactly one dominant element, readable in both light and dark host modes, all displayed numbers rounded.
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
