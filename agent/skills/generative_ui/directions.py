"""Aesthetic direction library — single source for guideline bundle, planning menu, and validators.

Edit HERE; then regenerate the top-level guideline artifacts:
    python -m agent.skills.generative_ui.bundler
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Direction:
    key: str
    menu_line: str
    spec_block: str


DIRECTIONS_INTRO = """## Aesthetic directions — pick ONE before coding

This is mandatory. Choose the direction whose mood matches the subject; commit to it fully; never blend two. Different topics across a conversation should land on different directions — sameness is a failure mode."""


DIRECTIONS: dict[str, Direction] = {
    "lab-dark": Direction(
        key="lab-dark",
        menu_line="dark precision stage, cyan/magenta glow, mono readouts — physics/chem/algorithm sims, particles, waves",
        spec_block="""**`lab-dark` — precision instrument.** Physics/chemistry/algorithm simulations; particles, fields, waves; anything animated on a stage.
- Surface: root panel `#131028` (deep violet — harmonizes with the host's dark cosmos), `border-radius: 16px`, `padding: 20px`; faint gridlines `rgba(168,155,190,.10)`
- Ink: `#E8E0F0` primary, `#A89BBE` muted · Accents (max 2): cyan `#22D3EE`, magenta `#F472B6`, amber `#FBBF24`
- Type: mono readouts (`ui-monospace, 'Cascadia Mono', Consolas, monospace`) with `font-variant-numeric: tabular-nums`; sans labels
- Motion: state 120ms linear; layout 350ms `cubic-bezier(.22,1,.36,1)`
- Signature: glow on live elements (`box-shadow: 0 0 12px rgba(34,211,238,.45)` or canvas shadowBlur), hairline tick rulers along axes
- Kit: button `background:#241D40; border:1px solid rgba(168,155,190,.25); border-radius:8px`, hover `#2E2553`, active `scale(.97)` · slider track `#2E2553` + thumb `#22D3EE` with glow · inner stage `#0F0C20`, radius 12 · label 12px uppercase `letter-spacing:.08em` `#A89BBE`""",
    ),
    "paper-editorial": Direction(
        key="paper-editorial",
        menu_line="warm paper, serif display, terracotta/moss — poetry, literature, history, language, philosophy",
        spec_block="""**`paper-editorial` — warm print.** Poetry, literature, history, philosophy, language, storytelling.
- Surface: panel `#FAF6EE` (`@media (prefers-color-scheme: dark)`: `#221E18`), ink `#272420` (dark `#E8E2D6`)
- Accents: terracotta `#C2410C`, moss `#4D7C0F`
- Type: serif display (`Georgia, 'Times New Roman', serif`) 26–32px for the lead element; body 16px / line-height 1.75
- Motion: 450ms opacity/transform fades only; nothing bounces
- Signature: 1px hairline rules `#D6CDBD`, an oversized serif quotation mark or drop cap, generous margins
- Kit: button transparent with `1px solid #C2410C; color:#C2410C`, hover fills `#C2410C` with `#FAF6EE` text · inner card `#FFFDF8` with hairline border · drop cap `float:left; font-size:54px; line-height:.85; padding-right:8px` · divider: centered `· · ·` or 1px rule""",
    ),
    "studio-pop": Direction(
        key="studio-pop",
        menu_line="white + bold geometric color blocks, hard offset shadows — art, design, music, playful or kid-facing topics",
        spec_block="""**`studio-pop` — gallery poster.** Art, design, music, creative showcases, playful or kid-facing topics.
- Surface: `#FFFFFF` (dark `#18181B`) with large geometric color blocks
- Accents (pick 2): electric violet `#7C3AED`, lemon `#FDE047`, hot coral `#FB7185`, mint `#5EEAD4`
- Type: sans 700 display, `letter-spacing: -0.02em`, oversized numerals
- Motion: snappy 160ms ease-out; hover lifts the element
- Signature: 2–3px solid borders, hard offset shadows (`box-shadow: 4px 4px 0 #18181B`), circular badges
- Kit: button `border:3px solid #18181B; box-shadow:3px 3px 0 #18181B; font-weight:700`, hover `translate(-2px,-2px)` + `box-shadow:5px 5px 0 #18181B`, active `translate(0,0)` + `box-shadow:2px 2px 0 #18181B` · tile: solid accent block with 3px border · badge: circle, lemon bg, 700 weight""",
    ),
    "terminal-data": Direction(
        key="terminal-data",
        menu_line="charcoal, mono tabular numerals, green/red deltas — finance, metrics, performance dashboards",
        spec_block="""**`terminal-data` — trading desk.** Finance, metrics, performance, engineering dashboards, logs.
- Surface: panel `#17141F` (violet-charcoal — harmonizes with the host's dark cosmos); or light variant `#F8F6FB` with ink `#1A1A2E`
- Ink: `#D6D2DE` · positive `#34D399`, negative `#F87171`, neutral accent `#A78BFA`
- Type: mono numerals, `font-variant-numeric: tabular-nums`; 11–12px uppercase labels with `letter-spacing: .08em`
- Motion: numbers count up 400ms; bars grow 400ms ease-out; zero decorative motion
- Signature: 1px dotted gridlines `rgba(168,155,190,.25)`, sparklines, ▲/▼ deltas in semantic color
- Kit: button `1px solid rgba(168,155,190,.3)`, mono 12px uppercase, hover `border-color:#A78BFA` · delta chip: `▲ +4.2%` in `#34D399` / `▼ -1.8%` in `#F87171`, mono · row dividers `1px dotted rgba(168,155,190,.2)` · metric card `#1F1A2D`, radius 8""",
    ),
    "soft-organic": Direction(
        key="soft-organic",
        menu_line="cream + sage/clay blob shapes, breathing motion — biology, nature, health, food, emotions",
        spec_block="""**`soft-organic` — field notebook.** Biology, nature, health, food, environment, emotions.
- Surface: cream `#FBF9F4` (dark `#1F231F`); shapes in sage `#84A98C`, clay `#E07A5F`, pine `#3A5A50`
- Type: sans, roomy spacing
- Motion: 500ms ease-in-out; slow breathing loops (`transform: scale(1)↔scale(1.03)`) for living things
- Signature: blob radii (`border-radius: 58% 42% 55% 45% / 48% 55% 45% 52%`), layered translucent circles, leaf/petal accents drawn as SVG paths
- Kit: button pill `border-radius:999px; background:#84A98C; color:#FFF`, hover `scale(1.04)` + deepen to `#6E927A`, active `scale(.98)` · inner card `#FFFFFF` on cream, radius 20–24 · tag pill clay `#E07A5F` · readout: layered translucent sage circles behind the number""",
    ),
    "blueprint": Direction(
        key="blueprint",
        menu_line="pale grid + indigo ink, dashed construction lines — mechanics, architecture, how-things-work cutaways",
        spec_block="""**`blueprint` — engineer's drawing.** Architecture, mechanics, hardware, how-things-work cutaways.
- Surface: pale grid `#F4F7FB` with ink `#1E4D8C` (dark: `#0C1D33` with ink `#9DC2EB`)
- Accent: one warm highlight `#D97706` for the active part
- Type: mono labels with `letter-spacing: .05em`; 12px dimension numerals
- Motion: 200ms linear; parts slide along axes (transform only)
- Signature: dashed construction lines (`stroke-dasharray: 6 4`), measurement arrows with end ticks, corner crop marks
- Kit: grid surface `background-image: linear-gradient(rgba(30,77,140,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(30,77,140,.07) 1px, transparent 1px); background-size: 24px 24px` · button `1px solid #1E4D8C; color:#1E4D8C`, mono, `border-radius:2px`, hover `rgba(30,77,140,.08)` · callout box: 1px dashed border · active part: `#D97706` fill/stroke""",
    ),
    "ink-wash": Direction(
        key="ink-wash",
        menu_line="raw paper + layered ink ridgelines, seal-red accent — classical Chinese subjects: poetry, landscape, calligraphy, tea",
        spec_block="""**`ink-wash` — 水墨 scroll.** Classical Chinese subjects: poetry imagery, landscape, calligraphy, tea, traditional culture.
- Surface: raw paper `#F5F1E8` (a physical scene — do NOT invert with the host theme); ink is `#2A2D30` at layered opacities (far `.18` / mid `.30` / near `.52`)
- Accents (tiny doses only): seal vermilion `#9E2B22`, moon gold `#E5C158`
- Type: serif (`Georgia, 'Times New Roman', 'Noto Serif SC', serif`); hanzi tracked out (`letter-spacing: .3em`); short titles may run vertical (`writing-mode: vertical-rl`)
- Motion: slow ink reveals — opacity 600–900ms ease; nothing bounces, nothing glows
- Signature: layered noise ridgelines with atmospheric perspective (farther = paler + smoother), one red seal stamp, generous 留白 — the empty space IS the composition
- Kit: panel radius 6px · button `1px solid #2A2D30`, serif, tracked, hover inverts to ink bg with paper text · seal: `writing-mode:vertical-rl` on `#9E2B22`, slight rotate · mist: translucent paper-colored horizontal bands between ridge layers · scenery is GENERATED, not hand-placed — use the algorithmic scenery recipes""",
    ),
    "host-calm": Direction(
        key="host-calm",
        menu_line="app-native quiet, host CSS variables — data records, forms, business UI mockups",
        spec_block="""**`host-calm` — quiet native.** Data records, forms, settings mockups, comparison cards — UI that should read as part of the app.
- Surface: transparent root; cards `var(--color-background-primary)`, `0.5px solid var(--color-border-tertiary)`, `border-radius: var(--border-radius-lg)`
- Ink: `var(--color-text-primary)` / `var(--color-text-secondary)` · Accents: host semantic vars + the 9 SVG color ramps
- Type: `var(--font-sans)`, weights 400/500
- Motion: 150ms ease; hover `var(--color-background-secondary)`; active `scale(0.98)`
- Signature: restraint — generous whitespace, hairline dividers, a single 2px accent border on the featured item
- Kit: controls as bare tags (host pre-styles them) · metric card `var(--color-background-secondary)`, no border, radius-md, 13px muted label over 24px/500 number · chip: `0.5px` border pill, active state `var(--color-background-info)` + `var(--color-text-info)`""",
    ),
}


def render_directions_block() -> str:
    """Full library for the guideline bundle: intro + every direction spec."""
    specs = "\n\n".join(d.spec_block for d in DIRECTIONS.values())
    return DIRECTIONS_INTRO + "\n\n" + specs


def render_direction_menu() -> str:
    """One line per direction, for the planning prompt."""
    return "\n".join(f"- {d.key}: {d.menu_line}" for d in DIRECTIONS.values())
