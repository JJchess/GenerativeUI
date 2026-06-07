"""Aesthetic direction library — single source for guideline bundle, planning menu, and future validators.

Generated initially from guidelines/CORE.md; edit HERE from now on.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Direction:
    key: str
    menu_line: str
    spec_block: str


DIRECTIONS_INTRO = '## Aesthetic directions — pick ONE before coding\n\nThis is mandatory. Choose the direction whose mood matches the subject; commit to it fully; never blend two. Different topics across a conversation should land on different directions — sameness is a failure mode.'

DIRECTIONS: dict[str, Direction] = {
    'lab-dark': Direction(
        key='lab-dark',
        menu_line='dark precision stage, cyan/magenta glow, mono readouts — physics/chem/algorithm sims, particles, waves',
        spec_block="**`lab-dark` — precision instrument.** Physics/chemistry/algorithm simulations; particles, fields, waves; anything animated on a stage.\n- Surface: root panel `#0D1322`, `border-radius: 16px`, `padding: 20px`; faint gridlines `rgba(148,163,184,.08)`\n- Ink: `#E2E8F0` primary, `#94A3B8` muted · Accents (max 2): cyan `#22D3EE`, magenta `#F472B6`, amber `#FBBF24`\n- Type: mono readouts (`ui-monospace, 'Cascadia Mono', Consolas, monospace`) with `font-variant-numeric: tabular-nums`; sans labels\n- Motion: state 120ms linear; layout 350ms `cubic-bezier(.22,1,.36,1)`\n- Signature: glow on live elements (`box-shadow: 0 0 12px rgba(34,211,238,.45)` or canvas shadowBlur), hairline tick rulers along axes",
    ),
    'paper-editorial': Direction(
        key='paper-editorial',
        menu_line='warm paper, serif display, terracotta/moss — poetry, literature, history, language, philosophy',
        spec_block="**`paper-editorial` — warm print.** Poetry, literature, history, philosophy, language, storytelling.\n- Surface: panel `#FAF6EE` (`@media (prefers-color-scheme: dark)`: `#221E18`), ink `#272420` (dark `#E8E2D6`)\n- Accents: terracotta `#C2410C`, moss `#4D7C0F`\n- Type: serif display (`Georgia, 'Times New Roman', serif`) 26–32px for the lead element; body 16px / line-height 1.75\n- Motion: 450ms opacity/transform fades only; nothing bounces\n- Signature: 1px hairline rules `#D6CDBD`, an oversized serif quotation mark or drop cap, generous margins",
    ),
    'studio-pop': Direction(
        key='studio-pop',
        menu_line='white + bold geometric color blocks, hard offset shadows — art, design, music, playful or kid-facing topics',
        spec_block='**`studio-pop` — gallery poster.** Art, design, music, creative showcases, playful or kid-facing topics.\n- Surface: `#FFFFFF` (dark `#18181B`) with large geometric color blocks\n- Accents (pick 2): electric blue `#2563EB`, lemon `#FDE047`, hot coral `#FB7185`, mint `#5EEAD4`\n- Type: sans 700 display, `letter-spacing: -0.02em`, oversized numerals\n- Motion: snappy 160ms ease-out; hover lifts the element\n- Signature: 2–3px solid borders, hard offset shadows (`box-shadow: 4px 4px 0 #18181B`), circular badges',
    ),
    'terminal-data': Direction(
        key='terminal-data',
        menu_line='charcoal, mono tabular numerals, green/red deltas — finance, metrics, performance dashboards',
        spec_block='**`terminal-data` — trading desk.** Finance, metrics, performance, engineering dashboards, logs.\n- Surface: panel `#15171C`; or light variant `#F8FAFC` with ink `#0F172A`\n- Ink: `#D1D5DB` · positive `#34D399`, negative `#F87171`, neutral accent `#60A5FA`\n- Type: mono numerals, `font-variant-numeric: tabular-nums`; 11–12px uppercase labels with `letter-spacing: .08em`\n- Motion: numbers count up 400ms; bars grow 400ms ease-out; zero decorative motion\n- Signature: 1px dotted gridlines `rgba(148,163,184,.25)`, sparklines, ▲/▼ deltas in semantic color',
    ),
    'soft-organic': Direction(
        key='soft-organic',
        menu_line='cream + sage/clay blob shapes, breathing motion — biology, nature, health, food, emotions',
        spec_block='**`soft-organic` — field notebook.** Biology, nature, health, food, environment, emotions.\n- Surface: cream `#FBF9F4` (dark `#1F231F`); shapes in sage `#84A98C`, clay `#E07A5F`, pine `#3A5A50`\n- Type: sans, roomy spacing\n- Motion: 500ms ease-in-out; slow breathing loops (`transform: scale(1)↔scale(1.03)`) for living things\n- Signature: blob radii (`border-radius: 58% 42% 55% 45% / 48% 55% 45% 52%`), layered translucent circles, leaf/petal accents drawn as SVG paths',
    ),
    'blueprint': Direction(
        key='blueprint',
        menu_line='pale grid + indigo ink, dashed construction lines — mechanics, architecture, how-things-work cutaways',
        spec_block="**`blueprint` — engineer's drawing.** Architecture, mechanics, hardware, how-things-work cutaways.\n- Surface: pale grid `#F4F7FB` with ink `#1E4D8C` (dark: `#0C1D33` with ink `#9DC2EB`)\n- Accent: one warm highlight `#D97706` for the active part\n- Type: mono labels with `letter-spacing: .05em`; 12px dimension numerals\n- Motion: 200ms linear; parts slide along axes (transform only)\n- Signature: dashed construction lines (`stroke-dasharray: 6 4`), measurement arrows with end ticks, corner crop marks",
    ),
    'host-calm': Direction(
        key='host-calm',
        menu_line='app-native quiet, host CSS variables — data records, forms, business UI mockups',
        spec_block='**`host-calm` — quiet native.** Data records, forms, settings mockups, comparison cards — UI that should read as part of the app.\n- Surface: transparent root; cards `var(--color-background-primary)`, `0.5px solid var(--color-border-tertiary)`, `border-radius: var(--border-radius-lg)`\n- Ink: `var(--color-text-primary)` / `var(--color-text-secondary)` · Accents: host semantic vars + the 9 SVG color ramps\n- Type: `var(--font-sans)`, weights 400/500\n- Motion: 150ms ease; hover `var(--color-background-secondary)`; active `scale(0.98)`\n- Signature: restraint — generous whitespace, hairline dividers, a single 2px accent border on the featured item',
    ),
}


def render_directions_block() -> str:
    """Full library for the guideline bundle: intro + every direction spec."""
    specs = "\n\n".join(d.spec_block for d in DIRECTIONS.values())
    return DIRECTIONS_INTRO + "\n\n" + specs


def render_direction_menu() -> str:
    """One line per direction, for the planning prompt."""
    return "\n".join(f"- {d.key}: {d.menu_line}" for d in DIRECTIONS.values())
