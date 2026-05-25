from __future__ import annotations

from typing import Dict

VISUAL_TRIGGERS_ZH = [
    "演示",
    "可视化",
    "图表",
    "交互式",
    "交互",
    "仿真",
    "模拟",
    "动画",
    "流程图",
    "界面",
    "组件",
    "展示",
]

VISUAL_TRIGGERS_EN = [
    "visual",
    "widget",
    "chart",
    "diagram",
    "interactive",
    "simulation",
    "dashboard",
    "graph",
]

WIDGET_TYPES = (
    "interactive",
    "chart",
    "chart_interactive",
    "mockup",
    "art",
    "art_interactive",
    "diagram",
)

MODULE_GUIDANCE: Dict[str, str] = {
    "interactive": (
        "Build an explorable demo with clear controls. Prefer sliders, buttons, toggles, or draggable inputs. "
        "Show one core interaction rather than many unrelated controls."
    ),
    "chart": (
        "Focus on data readability. Good axes, legends, labels, and readable color contrast matter more than decoration. "
        "Prefer lightweight SVG or canvas charts over heavy libraries unless truly needed."
    ),
    "chart_interactive": (
        "Combine a chart with one or two meaningful controls such as filter, range, or comparison toggle. "
        "Interaction must change the data view clearly."
    ),
    "mockup": (
        "Render a clean UI mockup with cards, forms, panels, and layout hierarchy. "
        "No fake browser chrome, no heavy shadows, and no unnecessary filler copy."
    ),
    "art": (
        "Create a visual scene or illustration with pure HTML/SVG/CSS/JS. "
        "Keep it elegant, flat, and deterministic."
    ),
    "art_interactive": (
        "Create a visual scene with one simple playful interaction, such as play/pause, scrub, or hover reaction."
    ),
    "diagram": (
        "Produce a structural SVG or HTML diagram with a very clear information hierarchy. "
        "Keep text sparse and use arrows, grouping, or lanes only when they clarify meaning."
    ),
}

CORE_GUIDANCE = """
You create inline visual content for chat. The output must be a self-contained HTML fragment.

Hard rules:
- Return fragment only. No <!doctype>, <html>, <head>, or <body>.
- Use flat design. No gradients, glow, blur, or decorative shadows.
- Use normal readable text sizes. Never smaller than 11px.
- Keep external dependencies to zero unless unavoidable.
- Prefer structure order: <style> then markup then <script>.
- The fragment must contain at least one of: <div>, <svg>, <canvas>, <style>.
- Keep it robust inside an iframe with sandbox='allow-scripts'.
- Use only light explanatory text inside the widget. No long essay inside the widget.
- Make dark-on-light defaults so the iframe is readable immediately.
- If there is interaction, wire it with plain browser JavaScript.
""".strip()
