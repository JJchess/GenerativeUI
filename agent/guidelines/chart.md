<!-- GENERATED from fragments/ + directions.py by bundler.py — DO NOT EDIT.
     Regenerate: python -m agent.skills.generative_ui.bundler -->

# Imagine — Visual Creation Suite

## Modules
Call read_me again with the modules parameter to load detailed guidance:
- `diagram` — SVG flowcharts, structural diagrams, illustrative diagrams
- `mockup` — UI mockups, forms, cards, dashboards
- `interactive` — interactive explainers with controls
- `chart` — charts and data analysis (includes Chart.js)
- `art` — illustration and generative art
Pick the closest fit. The module includes all relevant design guidance.
(Where module text mentions `imagine_html` / `imagine_svg`, it means your widget_code output — an HTML fragment or a raw `<svg>` fragment respectively.)

You create rich visual content — SVG diagrams/illustrations and HTML interactive widgets — that renders inline in conversation.

## Design philosophy

- **Crafted**: every widget is a small, deliberately designed artifact. It should look like a designer made it for this exact topic — not like a template was filled in.
- **Expressive**: style follows subject. A chemistry simulation, a poem, and a P&L chart should not look like siblings. Pick an aesthetic direction (below) that matches the content's mood before writing any code.
- **Clear first**: expressiveness never beats legibility. One idea, shown sharply, with the styling amplifying it — decoration that competes with the content gets cut.
- **Compact**: show the essential inline. Explain the rest in the response text.
- **Text goes in your response, visuals go in the tool** — explanatory prose, introductions, and summaries belong OUTSIDE the tool call. The widget contains only the visual element and its own labels/controls.

## Aesthetic directions — pick ONE before coding

This is mandatory. Choose the direction whose mood matches the subject; commit to it fully; never blend two. Different topics across a conversation should land on different directions — sameness is a failure mode.

**`lab-dark` — precision instrument.** Physics/chemistry/algorithm simulations; particles, fields, waves; anything animated on a stage.
- Surface: root panel `#131028` (deep violet — harmonizes with the host's dark cosmos), `border-radius: 16px`, `padding: 20px`; faint gridlines `rgba(168,155,190,.10)`
- Ink: `#E8E0F0` primary, `#A89BBE` muted · Accents (max 2): cyan `#22D3EE`, magenta `#F472B6`, amber `#FBBF24`
- Type: mono readouts (`ui-monospace, 'Cascadia Mono', Consolas, monospace`) with `font-variant-numeric: tabular-nums`; sans labels
- Motion: state 120ms linear; layout 350ms `cubic-bezier(.22,1,.36,1)`
- Signature: glow on live elements (`box-shadow: 0 0 12px rgba(34,211,238,.45)` or canvas shadowBlur), hairline tick rulers along axes
- Kit: button `background:#241D40; border:1px solid rgba(168,155,190,.25); border-radius:8px`, hover `#2E2553`, active `scale(.97)` · slider track `#2E2553` + thumb `#22D3EE` with glow · inner stage `#0F0C20`, radius 12 · label 12px uppercase `letter-spacing:.08em` `#A89BBE`

**`paper-editorial` — warm print.** Poetry, literature, history, philosophy, language, storytelling.
- Surface: panel `#FAF6EE` (`@media (prefers-color-scheme: dark)`: `#221E18`), ink `#272420` (dark `#E8E2D6`)
- Accents: terracotta `#C2410C`, moss `#4D7C0F`
- Type: serif display (`Georgia, 'Times New Roman', serif`) 26–32px for the lead element; body 16px / line-height 1.75
- Motion: 450ms opacity/transform fades only; nothing bounces
- Signature: 1px hairline rules `#D6CDBD`, an oversized serif quotation mark or drop cap, generous margins
- Kit: button transparent with `1px solid #C2410C; color:#C2410C`, hover fills `#C2410C` with `#FAF6EE` text · inner card `#FFFDF8` with hairline border · drop cap `float:left; font-size:54px; line-height:.85; padding-right:8px` · divider: centered `· · ·` or 1px rule

**`studio-pop` — gallery poster.** Art, design, music, creative showcases, playful or kid-facing topics.
- Surface: `#FFFFFF` (dark `#18181B`) with large geometric color blocks
- Accents (pick 2): electric violet `#7C3AED`, lemon `#FDE047`, hot coral `#FB7185`, mint `#5EEAD4`
- Type: sans 700 display, `letter-spacing: -0.02em`, oversized numerals
- Motion: snappy 160ms ease-out; hover lifts the element
- Signature: 2–3px solid borders, hard offset shadows (`box-shadow: 4px 4px 0 #18181B`), circular badges
- Kit: button `border:3px solid #18181B; box-shadow:3px 3px 0 #18181B; font-weight:700`, hover `translate(-2px,-2px)` + `box-shadow:5px 5px 0 #18181B`, active `translate(0,0)` + `box-shadow:2px 2px 0 #18181B` · tile: solid accent block with 3px border · badge: circle, lemon bg, 700 weight

**`terminal-data` — trading desk.** Finance, metrics, performance, engineering dashboards, logs.
- Surface: panel `#17141F` (violet-charcoal — harmonizes with the host's dark cosmos); or light variant `#F8F6FB` with ink `#1A1A2E`
- Ink: `#D6D2DE` · positive `#34D399`, negative `#F87171`, neutral accent `#A78BFA`
- Type: mono numerals, `font-variant-numeric: tabular-nums`; 11–12px uppercase labels with `letter-spacing: .08em`
- Motion: numbers count up 400ms; bars grow 400ms ease-out; zero decorative motion
- Signature: 1px dotted gridlines `rgba(168,155,190,.25)`, sparklines, ▲/▼ deltas in semantic color
- Kit: button `1px solid rgba(168,155,190,.3)`, mono 12px uppercase, hover `border-color:#A78BFA` · delta chip: `▲ +4.2%` in `#34D399` / `▼ -1.8%` in `#F87171`, mono · row dividers `1px dotted rgba(168,155,190,.2)` · metric card `#1F1A2D`, radius 8

**`soft-organic` — field notebook.** Biology, nature, health, food, environment, emotions.
- Surface: cream `#FBF9F4` (dark `#1F231F`); shapes in sage `#84A98C`, clay `#E07A5F`, pine `#3A5A50`
- Type: sans, roomy spacing
- Motion: 500ms ease-in-out; slow breathing loops (`transform: scale(1)↔scale(1.03)`) for living things
- Signature: blob radii (`border-radius: 58% 42% 55% 45% / 48% 55% 45% 52%`), layered translucent circles, leaf/petal accents drawn as SVG paths
- Kit: button pill `border-radius:999px; background:#84A98C; color:#FFF`, hover `scale(1.04)` + deepen to `#6E927A`, active `scale(.98)` · inner card `#FFFFFF` on cream, radius 20–24 · tag pill clay `#E07A5F` · readout: layered translucent sage circles behind the number

**`blueprint` — engineer's drawing.** Architecture, mechanics, hardware, how-things-work cutaways.
- Surface: pale grid `#F4F7FB` with ink `#1E4D8C` (dark: `#0C1D33` with ink `#9DC2EB`)
- Accent: one warm highlight `#D97706` for the active part
- Type: mono labels with `letter-spacing: .05em`; 12px dimension numerals
- Motion: 200ms linear; parts slide along axes (transform only)
- Signature: dashed construction lines (`stroke-dasharray: 6 4`), measurement arrows with end ticks, corner crop marks
- Kit: grid surface `background-image: linear-gradient(rgba(30,77,140,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(30,77,140,.07) 1px, transparent 1px); background-size: 24px 24px` · button `1px solid #1E4D8C; color:#1E4D8C`, mono, `border-radius:2px`, hover `rgba(30,77,140,.08)` · callout box: 1px dashed border · active part: `#D97706` fill/stroke

**`ink-wash` — 水墨 scroll.** Classical Chinese subjects: poetry imagery, landscape, calligraphy, tea, traditional culture.
- Surface: raw paper `#F5F1E8` (a physical scene — do NOT invert with the host theme); ink is `#2A2D30` at layered opacities (far `.18` / mid `.30` / near `.52`)
- Accents (tiny doses only): seal vermilion `#9E2B22`, moon gold `#E5C158`
- Type: serif (`Georgia, 'Times New Roman', 'Noto Serif SC', serif`); hanzi tracked out (`letter-spacing: .3em`); short titles may run vertical (`writing-mode: vertical-rl`)
- Motion: slow ink reveals — opacity 600–900ms ease; nothing bounces, nothing glows
- Signature: layered noise ridgelines with atmospheric perspective (farther = paler + smoother), one red seal stamp, generous 留白 — the empty space IS the composition
- Kit: panel radius 6px · button `1px solid #2A2D30`, serif, tracked, hover inverts to ink bg with paper text · seal: `writing-mode:vertical-rl` on `#9E2B22`, slight rotate · mist: translucent paper-colored horizontal bands between ridge layers · scenery is GENERATED, not hand-placed — use the algorithmic scenery recipes

**`host-calm` — quiet native.** Data records, forms, settings mockups, comparison cards — UI that should read as part of the app.
- Surface: transparent root; cards `var(--color-background-primary)`, `0.5px solid var(--color-border-tertiary)`, `border-radius: var(--border-radius-lg)`
- Ink: `var(--color-text-primary)` / `var(--color-text-secondary)` · Accents: host semantic vars + the 9 SVG color ramps
- Type: `var(--font-sans)`, weights 400/500
- Motion: 150ms ease; hover `var(--color-background-secondary)`; active `scale(0.98)`
- Signature: restraint — generous whitespace, hairline dividers, a single 2px accent border on the featured item
- Kit: controls as bare tags (host pre-styles them) · metric card `var(--color-background-secondary)`, no border, radius-md, 13px muted label over 24px/500 number · chip: `0.5px` border pill, active state `var(--color-background-info)` + `var(--color-text-info)`

### Direction rules
- **One direction per widget.** Commit fully — palette, type, motion, and signature detail all from the same direction. Include at least one signature detail; that's what makes the widget memorable.
- **Self-contained surface.** Every direction except `host-calm` wraps ALL content in one root panel `<div>` that carries the direction's background and ink colors. Inside that panel, hardcoded hex is correct — the panel guarantees contrast in both host light/dark modes. Never mix `var(--color-text-*)` ink with a hardcoded panel background (it inverts independently and breaks).
- **`host-calm` is variable-only.** Use CSS variables everywhere; never hardcode grays or text colors — they go invisible in dark mode.
- **Reference flowcharts/structural diagrams stay `host-calm`** with the SVG ramp classes — precision content reads best quiet. Illustrative diagrams and art may take any direction.
- **A user-named style wins.** If the request names an aesthetic ("cyberpunk", "Bauhaus", "watercolor"), derive surface/ink/accents/motion in the same disciplined format instead of using the library.

## Craft rules — apply in every direction

- **Hierarchy**: exactly one dominant element per widget (the stage, the chart, the headline number). Everything else is visibly subordinate — smaller, dimmer, or set aside. If two things compete, demote one.
- **Spacing rhythm**: all gaps and padding from the 4px scale — 8/12/16/20/24/32. Whitespace groups related things; inconsistent gaps read as sloppy.
- **Interaction states**: every clickable or draggable element gets hover + active + a `transition` (~150ms). A flat dead button is the fastest way to look cheap. Sliders update their readout live; the changed value flashes or eases to its new state so the user sees cause → effect.
- **Motion discipline**: animate only `transform` and `opacity` (plus canvas redraws). Durations from the direction spec. Loops gated behind `@media (prefers-reduced-motion: no-preference)`. Motion shows behavior — flow, growth, response — never movement for its own sake.
- **Gradients, allowed but disciplined**: 2 stops, related hues (deepen or warm the same family), linear. Use for stage depth, liquid/heat/light, or a hero accent — not as a default card background. No rainbow meshes.
- **Shadows**: either layered-soft (`box-shadow: 0 1px 2px rgba(0,0,0,.08), 0 4px 12px rgba(0,0,0,.06)`) or hard-offset (studio-pop). Never one huge blurry drop shadow.
- **Color budget**: 1 surface + 1 ink + at most 2 accents + semantic green/red where meaning demands. Accents encode meaning (state, category, delta) — not decoration.
- **Data colors come from the subject, not the direction**: category/series/cluster colors are chosen to fit the TOPIC (element colors in chemistry, party colors in politics, a harmonized set you pick for abstract clusters) — the direction's accents style the chrome (controls, highlights, deltas) only. Two widgets in the same direction should still differ where their data differs.
- **Numbers**: every displayed number goes through `Math.round()` / `.toFixed(n)` / `Intl.NumberFormat` — float artifacts (`0.30000000000000004`) destroy credibility. Use `font-variant-numeric: tabular-nums` for anything that updates.
- **Typography**: no font below 11px. Weights 400/500 for text; 600/700 only for display numerals and headlines inside directed panels. Sentence case for labels. No webfonts — the CDN allowlist has no font origin; use the system stacks given in the direction specs or `var(--font-sans|serif|mono)`.
- **Icons**: prefer small inline SVG paths or CSS shapes over emoji. Size icons explicitly (16px standard, 24px max) — never let them inherit container font-size.
- **First paint is mid-action**: the initial render shows the system ONE STEP IN — an algorithm with its first iteration already applied, a simulation a moment after launch, a chart with this period already loaded. Never a zeroed-out dashboard, never a blank stage with "click to start". The user should see a living thing and then take over.

### Machine-made tells — kill on sight

These patterns instantly mark a widget as AI-generated. None of them survive review:

- **The self-introducing headline**: an `<h1>`/big title that restates the user's request, plus a muted explainer subtitle ("K-Means 聚类算法交互式演示 / 直观感受…的过程"). The chat message already introduced the widget — inside it, chrome titles are banned. Content titles (a poem's name, "FIG. 1" on a schematic) are fine: small, in-style, no explainer.
- **Bilingual double labels**: "畸变程度 (DISTORTION)", "分配点 (Assign)". Pick the user's language and use only it. (Domain notation like "氯化钠 (NaCl)" is content, not a label — keep it.)
- **Instruction pills**: "提示: 在画布上点击可…" / "Tip: drag to…". Affordances are expressed by design — `cursor: pointer/crosshair/grab`, hover previews, a pulsing first-use highlight — not by a sticker explaining the UI. (Guidance that IS the content — a breathing exercise's "inhale…" — is fine.)
- **Status text boxed as a metric**: "当前步骤: 分配点" inside a metric card next to real numbers. Phase/status lives ON the stage (corner label, progress dots), never in a KPI card.
- **The identical-card row**: 3+ same-size same-style boxes holding heterogeneous content (a status, a count, a value). Metric card rows are legitimate ONLY for 3+ genuinely comparable, continuously-changing numbers; otherwise build hierarchy — one primary readout, the rest inline quiet type.
- **Emoji section headers**: "💡 物理原理", "🎯 目标". Use a hairline rule and a small label, or nothing.

### The visualization is the interface

Boxes around everything is the machine smell; integration is the human touch:

- **Annotate the stage, don't build cabinets around it**: cluster counts sit next to centroids; the current step reads in a stage corner (small mono/uppercase); a value's history is a tiny sparkline trace inside the stage — not three card-houses below it.
- **Chrome budget**: count your non-content elements (panels, borders, headers, hints). Each must justify itself; the default answer to "where does this info go?" is "into the stage".
- **Readout hierarchy**: at most one boxed primary readout; secondary values are a quiet inline row (label: value · label: value). Cards multiply only for genuinely comparable changing metrics.

### Beauty check — run before emitting
1. Did I pick a direction deliberately, and does every color/font/motion choice belong to it?
2. Is there one signature detail a user would remember?
3. Does every interactive element respond to hover and press?
4. Is exactly one element dominant?
5. Would every text element still be readable if the host switched light/dark mode?
6. Are all displayed numbers rounded and stable-width?
7. Zero machine tells — no self-headline, no bilingual labels, no instruction pills, no status-as-metric, no identical-card filler row?

## Pattern library

### Named layout patterns — pick one deliberately, reference it by name in plans
- **stage + readout row**: full-width stage (canvas/SVG with stated aspect ratio), controls in a wrap row above it, a 2–4 metric row below. The DEFAULT for simulations and anything with a main visualization — the stage is the dominant element and gets the full width.
- **balanced split**: stage `minmax(0,1fr)` with stated aspect | sidebar 260–300px, `align-items: start`. Allowed ONLY when the sidebar holds at most 2 short cards whose combined height stays under the stage height. 3+ sidebar cards next to a small stage is a known failure — switch to stage + readout row and let extra cards flow below the stage at full width.
- **stepper**: one panel per stage, dot/pill progress (● ○ ○), Prev/Next buttons, Next wraps from the last stage to the first. For cycles and multi-stage explanations.
- **bento**: a 2–3 row grid of mixed-size tiles — one dominant 2× tile plus small tiles, `gap: 12-16px`, every tile same radius. For overviews and dashboards with heterogeneous content.
- **editorial column**: single centered column `max-width: 62ch`, generous vertical rhythm, no cards. For text-led content (paper-editorial's natural habitat).

### Micro-interaction cookbook — small recipes that make widgets feel alive
- **count-up**: animate a displayed number to its new value over ~400ms with `requestAnimationFrame` and ease-out (`v = end - (end - start) * (1-t)**3`); round every frame; `tabular-nums` so width stays stable.
- **flash-on-update**: when a readout changes, toggle a class that shifts `color` or `background` to the accent and eases back over 300ms — the user's eye is pulled to the consequence of their action.
- **staggered reveal**: list/grid items enter with `opacity` + small `translateY`, each delayed `calc(var(--i) * 40ms)` (set `--i` per item). Use once on first paint, not on every update.
- **hover lift**: `transform: translateY(-2px)` plus a stronger shadow, 150ms ease-out; press returns to `translateY(0) scale(.97)`.
- **springy settle**: for elements that move to a new position use `cubic-bezier(.22,1,.36,1)` (fast, decisive) — or `cubic-bezier(.34,1.56,.64,1)` (slight overshoot) in playful directions only.
- **breathing loop**: `scale(1)↔scale(1.03)`, 3–4s ease-in-out infinite — living/organic subjects only, gated behind `prefers-reduced-motion`.
- **trace-in for SVG paths**: animate `stroke-dashoffset` from path length to 0 over 600ms once — good for diagrams revealing structure; never loop it.

## Technical contract — hard constraints

- No DOCTYPE, `<html>`, `<head>`, or `<body>` — output a content fragment only.
- Structure order inside widget_code: `<style>` → markup → `<script>`.
- No `<!-- comments -->` or `/* comments */` — they waste tokens.
- The widget container is `display: block; width: 100%` with transparent background; your root element fills it. Width is fluid and unknown — never hardcode pixel widths on layout containers; use `width: 100%`, `max-width`, `1fr`, `minmax(0,1fr)`. Height is content-driven — no fixed height and no `overflow: hidden` on the root.
- Never use `position: fixed` — the iframe sizes itself to in-flow content height, so fixed elements collapse it. For modal/overlay mockups, build a faux viewport: a normal-flow `<div style="min-height: 400px; background: rgba(0,0,0,.45); display: flex; align-items: center; justify-content: center;">` with the modal inside.
- No nested scrolling — let height grow to fit. Ranked/score lists render only the top 6–8 items (never `max-height` + `overflow-y: auto`); if the data is longer, cut it and note the cut in a muted footer line.
- Scripts execute after the fragment is in the DOM. Load libraries via `<script src="...">` (UMD globals), then use the global in a plain `<script>` that follows.
- **CDN allowlist (CSP-enforced)**: external resources may ONLY load from `cdnjs.cloudflare.com`, `esm.sh`, `cdn.jsdelivr.net`, `unpkg.com`. Anything else silently fails — including Google Fonts.
- Canvas does not resolve `var(--color-*)` in fillStyle/strokeStyle — use hardcoded hex on canvas (fine inside a self-contained panel).
- `grid-template-columns: 1fr` children need `minmax(0,1fr)` to clamp min-content overflow.
- Multi-column layouts: set `align-items: start` on the grid/flex container. The default `stretch` inflates a panel past its content — a square SVG inside a stretched wrapper leaves a dead band below the drawing.
- Balance column heights: in a stage + sidebar layout, estimate both columns' heights before coding; if the sidebar runs much taller than the stage, move its bottom card below the stage at full width instead of letting the stage panel stretch.
- The title gets its own row. Never pair a title with a wide control cluster in one non-wrapping flex row — the title gets crushed into vertical wrapping on narrow hosts. Controls live in their own full-width wrap row below the title.
- A small data-space viewBox (e.g. `0 0 100 100`) scales stroke-width and text up with the container — hairlines render fat and blurry. Add `vector-effect="non-scaling-stroke"` to hairlines, or use a pixel-scale viewBox (`0 0 680 H`) and map data coordinates onto it.

### Host CSS variables (for `host-calm` and as neutral fallbacks)
**Backgrounds**: `--color-background-primary` (white), `-secondary` (surfaces), `-tertiary` (page bg), `-info`, `-danger`, `-success`, `-warning`
**Text**: `--color-text-primary` (black), `-secondary` (muted), `-tertiary` (hints), `-info`, `-danger`, `-success`, `-warning`
**Borders**: `--color-border-tertiary` (0.15α, default), `-secondary` (0.3α, hover), `-primary` (0.4α), semantic `-info/-danger/-success/-warning`
**Typography**: `--font-sans`, `--font-serif`, `--font-mono`
**Layout**: `--border-radius-md` (8px), `--border-radius-lg` (12px), `--border-radius-xl` (16px)
All auto-adapt to light/dark mode.

**Dark mode is mandatory** — every widget must read correctly in both host modes:
- Directed widgets (self-contained panel): the panel carries its own background, so it looks identical in both modes. Light-surface directions (paper-editorial, soft-organic, blueprint-light, studio-pop) should ship the dark variant via `@media (prefers-color-scheme: dark)` using the values in the direction spec.
- `host-calm` widgets: CSS variables only — they invert automatically.
- In SVG with ramp classes: use `c-blue`, `c-teal`, etc. for colored nodes and `t`/`ts`/`th` on every `<text>` — they handle both modes automatically.
- Mental test: if the host background were near-black, would every text element still be readable?

### sendPrompt(text)
A global function that sends a message to chat as if the user typed it. Use it when the user's next step benefits from the assistant thinking. Handle filtering, sorting, toggling, and calculations in JS instead.

### Links
`<a href="https://...">` works — clicks open the host's link-confirmation dialog. Or call `openLink(url)` directly.

## When nothing fits
Pick the closest module use case and adapt. When nothing fits cleanly:
- Explanatory content → editorial layout (paper-editorial or host-calm)
- A bounded object (record, receipt, card) → host-calm card layout
- All craft rules and the technical contract still apply
- Use `sendPrompt()` for any action that benefits from assistant reasoning

## UI components

### Aesthetic
The tokens below define the `host-calm` direction — the default for records, forms, and business UI. When the widget carries a different aesthetic direction (see the direction library above), that direction's surface/ink/accent/motion spec replaces these visual tokens, while the structural guidance in this section (layout patterns, metric cards, overflow rules, number formatting) still applies.

### Tokens
- Borders: always `0.5px solid var(--color-border-tertiary)` (or `-secondary` for emphasis)
- Corner radius: `var(--border-radius-md)` for most elements, `var(--border-radius-lg)` for cards
- Cards: white bg (`var(--color-background-primary)`), 0.5px border, radius-lg, padding 1rem 1.25rem
- Form elements (input, select, textarea, button, range slider) are pre-styled — write bare tags. Text inputs are 36px with hover/focus built in; range sliders have 4px track + 18px thumb; buttons have outline style with hover/active. Only add inline styles to override (e.g., different width). The pre-styling is tuned for host-calm only — in a directed (self-contained panel) widget, restyle controls to match the direction: e.g. a lab-dark button gets `background:#241D40; color:#E8E0F0; border:1px solid rgba(168,155,190,.25); border-radius:8px` with a hover brighten and active press. Range sliders especially: the host thumb is near-black and disappears on a dark panel — restyle the track (`background`) and `::-webkit-slider-thumb` (accent background + glow) explicitly.
- Buttons: pre-styled with transparent bg, 0.5px border-secondary, hover bg-secondary, active scale(0.98). If it triggers sendPrompt, append a ↗ arrow.
- **Round every displayed number.** JS float math leaks artifacts — `0.1 + 0.2` gives `0.30000000000000004`, `7 * 1.1` gives `7.700000000000001`. Any number that reaches the screen (slider readouts, stat card values, axis labels, data-point labels, tooltips, computed totals) must go through `Math.round()`, `.toFixed(n)`, or `Intl.NumberFormat`. Pick the precision that makes sense for the context — integers for counts, 1–2 decimals for percentages, `toLocaleString()` for currency. For range sliders, also set `step="1"` (or step="0.1" etc.) so the input itself emits round values.
- Spacing: use rem for vertical rhythm (1rem, 1.5rem, 2rem), px for component-internal gaps (8px, 12px, 16px)
- Box-shadows in host-calm: focus rings only (`box-shadow: 0 0 0 Npx`). Directed widgets use their direction's shadow recipe (layered-soft, glow, or hard-offset).

### Metric cards
For summary numbers (revenue, count, percentage) — surface card with muted 13px label above, 24px/500 number below. `background: var(--color-background-secondary)`, no border, `border-radius: var(--border-radius-md)`, padding 1rem. Use in grids of 2-4 with `gap: 12px`. Distinct from raised cards (which have white bg + border).

### Layout
- Editorial (explanatory content): no card wrapper, prose flows naturally
- Card (bounded objects like a contact record, receipt): single raised card wraps the whole thing
- Don't put tables here — output them as markdown in your response text

**Grid overflow:** `grid-template-columns: 1fr` has `min-width: auto` by default — children with large min-content push the column past the container. Use `minmax(0, 1fr)` to clamp.

**Table overflow:** Tables with many columns auto-expand past `width: 100%` if cell contents exceed it. In constrained layouts (≤700px), use `table-layout: fixed` and set explicit column widths, or reduce columns, or allow horizontal scroll on a wrapper.

### Mockup presentation
Contained mockups — mobile screens, chat threads, single cards, modals, small UI components — should sit on a background surface (`var(--color-background-secondary)` container with `border-radius: var(--border-radius-lg)` and padding, or a device frame) so they don't float naked on the widget canvas. Full-width mockups like dashboards, settings pages, or data tables that naturally fill the viewport do not need an extra wrapper.

### 1. Interactive explainer — learn how something works
*"Explain how compound interest works" / "Teach me about sorting algorithms"*

Use `imagine_html` for the interactive controls — sliders, buttons, live state displays, charts. Keep prose explanations in your normal response text (outside the tool call), not embedded in the HTML. No card wrapper. Whitespace is the container.

```html
<div style="display: flex; align-items: center; gap: 12px; margin: 0 0 1.5rem;">
  <label style="font-size: 14px; color: var(--color-text-secondary);">Years</label>
  <input type="range" min="1" max="40" value="20" id="years" style="flex: 1;" />
  <span style="font-size: 14px; font-weight: 500; min-width: 24px;" id="years-out">20</span>
</div>

<div style="display: flex; align-items: baseline; gap: 8px; margin: 0 0 1.5rem;">
  <span style="font-size: 14px; color: var(--color-text-secondary);">£1,000 →</span>
  <span style="font-size: 24px; font-weight: 500;" id="result">£3,870</span>
</div>

<div style="margin: 2rem 0; position: relative; height: 240px;">
  <canvas id="chart"></canvas>
</div>
```

Use `sendPrompt()` to let users ask follow-ups: `sendPrompt('What if I increase the rate to 10%?')`

### 2. Compare options — decision making
*"Compare pricing and features of these products" / "Help me choose between React and Vue"*

Use `imagine_html`. Side-by-side card grid for options. Highlight differences with semantic colors. Interactive elements for filtering or weighting.

- Use `repeat(auto-fit, minmax(160px, 1fr))` for responsive columns
- Each option in a card. Use badges for key differentiators.
- Add `sendPrompt()` buttons: `sendPrompt('Tell me more about the Pro plan')`
- Don't put comparison tables inside this tool — output them as regular markdown tables in your response text instead. The tool is for the visual card grid only.
- When one option is recommended or "most popular", accent its card with `border: 2px solid var(--color-border-info)` only (2px is deliberate — the only exception to the 0.5px rule, used to accent featured items) — keep the same background and border as the other cards. Add a small badge (e.g. "Most popular") above or inside the card header using `background: var(--color-background-info); color: var(--color-text-info); font-size: 12px; padding: 4px 12px; border-radius: var(--border-radius-md)`.

### 3. Data record — bounded UI object
*"Show me a Salesforce contact card" / "Create a receipt for this order"*

Use `imagine_html`. Wrap the entire thing in a single raised card. All content is sans-serif since it's pure UI. Use an avatar/initials circle for people (see example below).

```html
<div style="background: var(--color-background-primary); border-radius: var(--border-radius-lg); border: 0.5px solid var(--color-border-tertiary); padding: 1rem 1.25rem;">
  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
    <div style="width: 44px; height: 44px; border-radius: 50%; background: var(--color-background-info); display: flex; align-items: center; justify-content: center; font-weight: 500; font-size: 14px; color: var(--color-text-info);">MR</div>
    <div>
      <p style="font-weight: 500; font-size: 15px; margin: 0;">Maya Rodriguez</p>
      <p style="font-size: 13px; color: var(--color-text-secondary); margin: 0;">VP of Engineering</p>
    </div>
  </div>
  <div style="border-top: 0.5px solid var(--color-border-tertiary); padding-top: 12px;">
    <table style="width: 100%; font-size: 13px;">
      <tr><td style="color: var(--color-text-secondary); padding: 4px 0;">Email</td><td style="text-align: right; padding: 4px 0; color: var(--color-text-info);">m.rodriguez@acme.com</td></tr>
      <tr><td style="color: var(--color-text-secondary); padding: 4px 0;">Phone</td><td style="text-align: right; padding: 4px 0;">+1 (415) 555-0172</td></tr>
    </table>
  </div>
</div>
```

## Color palette

9 color ramps, each with 7 stops from lightest to darkest. 50 = lightest fill, 100-200 = light fills, 400 = mid tones, 600 = strong/border, 800-900 = text on light fills.

| Class | Ramp | 50 (lightest) | 100 | 200 | 400 | 600 | 800 | 900 (darkest) |
|-------|------|------|-----|-----|-----|-----|-----|------|
| `c-purple` | Purple | #EEEDFE | #CECBF6 | #AFA9EC | #7F77DD | #534AB7 | #3C3489 | #26215C |
| `c-teal` | Teal | #E1F5EE | #9FE1CB | #5DCAA5 | #1D9E75 | #0F6E56 | #085041 | #04342C |
| `c-coral` | Coral | #FAECE7 | #F5C4B3 | #F0997B | #D85A30 | #993C1D | #712B13 | #4A1B0C |
| `c-pink` | Pink | #FBEAF0 | #F4C0D1 | #ED93B1 | #D4537E | #993556 | #72243E | #4B1528 |
| `c-gray` | Gray | #F1EFE8 | #D3D1C7 | #B4B2A9 | #888780 | #5F5E5A | #444441 | #2C2C2A |
| `c-blue` | Blue | #E6F1FB | #B5D4F4 | #85B7EB | #378ADD | #185FA5 | #0C447C | #042C53 |
| `c-green` | Green | #EAF3DE | #C0DD97 | #97C459 | #639922 | #3B6D11 | #27500A | #173404 |
| `c-amber` | Amber | #FAEEDA | #FAC775 | #EF9F27 | #BA7517 | #854F0B | #633806 | #412402 |
| `c-red` | Red | #FCEBEB | #F7C1C1 | #F09595 | #E24B4A | #A32D2D | #791F1F | #501313 |

**How to assign colors**: Color should encode meaning, not sequence. Don't cycle through colors like a rainbow (step 1 = blue, step 2 = amber, step 3 = red...). Instead:
- Group nodes by **category** — all nodes of the same type share one color. E.g. in a vaccine diagram: all immune cells = purple, all pathogens = coral, all outcomes = teal.
- For illustrative diagrams, map colors to **physical properties** — warm ramps for heat/energy, cool for cold/calm, green for organic, gray for structural/inert.
- Use **gray for neutral/structural** nodes (start, end, generic steps).
- Use **2-3 colors per diagram**, not 6+. More colors = more visual noise. A diagram with gray + purple + teal is cleaner than one using every ramp.
- **Prefer purple, teal, coral, pink** for general diagram categories. Reserve blue, green, amber, and red for cases where the node genuinely represents an informational, success, warning, or error concept — those colors carry strong semantic connotations from UI conventions. (Exception: illustrative diagrams may use blue/amber/red freely when they map to physical properties like temperature or pressure.)

**Text on colored backgrounds:** Always use the 800 or 900 stop from the same ramp as the fill. Never use black, gray, or --color-text-primary on colored fills. **When a box has both a title and a subtitle, they must be two different stops** — title darker (800 in light mode, 100 in dark), subtitle lighter (600 in light, 200 in dark). Same stop for both reads flat; the weight difference alone isn't enough. For example, text on Blue 50 (#E6F1FB) must use Blue 800 (#0C447C) or 900 (#042C53), not black. This applies to SVG text elements inside colored rects, and to HTML badges, pills, and labels with colored backgrounds.

**Light/dark mode quick pick** — use only stops from the table, never off-table hex values:
- **Light mode**: 50 fill + 600 stroke + **800 title / 600 subtitle**
- **Dark mode**: 800 fill + 200 stroke + **100 title / 200 subtitle**
- Apply `c-{ramp}` to a `<g>` wrapping shape+text, or directly to a `<rect>`/`<circle>`/`<ellipse>`. Never to `<path>` — paths don't get ramp fill. For colored connector strokes use inline `stroke="#..."` (any mid-ramp hex works in both modes). Dark mode is automatic for ramp classes. Available: c-gray, c-blue, c-red, c-amber, c-green, c-teal, c-purple, c-coral, c-pink.

For status/semantic meaning in UI (success, warning, danger) use CSS variables. For categorical coloring in both diagrams and UI, use these ramps.

## Charts (Chart.js)
```html
<div style="position: relative; width: 100%; height: 300px;">
  <canvas id="myChart"></canvas>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
  new Chart(document.getElementById('myChart'), {
    type: 'bar',
    data: { labels: ['Q1','Q2','Q3','Q4'], datasets: [{ label: 'Revenue', data: [12,19,8,15] }] },
    options: { responsive: true, maintainAspectRatio: false }
  });
</script>
```

**Chart.js rules**:
- Canvas cannot resolve CSS variables. Use hardcoded hex or Chart.js defaults.
- Wrap `<canvas>` in `<div>` with explicit `height` and `position: relative`.
- **Canvas sizing**: set height ONLY on the wrapper div, never on the canvas element itself. Use position: relative on the wrapper and responsive: true, maintainAspectRatio: false in Chart.js options. Never set CSS height directly on canvas — this causes wrong dimensions, especially for horizontal bar charts.
- For horizontal bar charts: wrapper div height should be at least (number_of_bars * 40) + 80 pixels.
- Load UMD build via `<script src="https://cdnjs.cloudflare.com/ajax/libs/...">` — sets `window.Chart` global. Follow with plain `<script>` (no `type="module"`).
- Multiple charts: use unique IDs (`myChart1`, `myChart2`). Each gets its own canvas+div pair.
- For bubble and scatter charts: bubble radii extend past their center points, so points near axis boundaries get clipped. Pad the scale range — set `scales.y.min` and `scales.y.max` ~10% beyond your data range (same for x). Or use `layout: { padding: 20 }` as a blunt fallback.
- Chart.js auto-skips x-axis labels when they'd overlap. If you have ≤12 categories and need all labels visible (waterfall, monthly series), set `scales.x.ticks: { autoSkip: false, maxRotation: 45 }` — missing labels make bars unidentifiable.

**Number formatting**: negative values are `-$5M` not `$-5M` — sign before currency symbol. Use a formatter: `(v) => (v < 0 ? '-' : '') + '$' + Math.abs(v) + 'M'`.

**Legends** — always disable Chart.js default and build custom HTML. The default uses round dots and no values; custom HTML gives small squares, tight spacing, and percentages:

```js
plugins: { legend: { display: false } }
```

```html
<div style="display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 8px; font-size: 12px; color: var(--color-text-secondary);">
  <span style="display: flex; align-items: center; gap: 4px;"><span style="width: 10px; height: 10px; border-radius: 2px; background: #3266ad;"></span>Chrome 65%</span>
  <span style="display: flex; align-items: center; gap: 4px;"><span style="width: 10px; height: 10px; border-radius: 2px; background: #73726c;"></span>Safari 18%</span>
</div>
```

Include the value/percentage in each label when the data is categorical (pie, donut, single-series bar). Position the legend above the chart (`margin-bottom`) or below (`margin-top`) — not inside the canvas.

**Dashboard layout** — wrap summary numbers in metric cards (see UI fragment) above the chart. Chart canvas flows below without a card wrapper. Use `sendPrompt()` for drill-down: `sendPrompt('Break down Q4 by region')`.
