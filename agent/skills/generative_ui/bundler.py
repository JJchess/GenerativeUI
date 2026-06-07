"""Composes guideline bundles from orthogonal fragments.

Source of truth layout:
  agent/guidelines/fragments/core/*.md      — shared design core (philosophy, craft, layout, technical)
  agent/skills/generative_ui/directions.py  — aesthetic direction library (data)
  agent/guidelines/fragments/modules/*.md   — per-widget-type technical guidance
  agent/guidelines/fragments/planning/*.md  — planning-stage phrasings of shared rules
  agent/guidelines/fragments/examples/*     — few-shot widget code examples

The top-level agent/guidelines/<module>.md files are GENERATED artifacts for human
inspection and external-host file consumers. Regenerate them with:
    python -m agent.skills.generative_ui.bundler
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from .directions import render_directions_block

_GUIDELINES_DIR = Path(__file__).resolve().parents[2] / "guidelines"
_FRAGMENTS_DIR = _GUIDELINES_DIR / "fragments"

_GENERATED_HEADER = (
    "<!-- GENERATED from fragments/ + directions.py by bundler.py — DO NOT EDIT.\n"
    "     Regenerate: python -m agent.skills.generative_ui.bundler -->\n\n"
)

# Ordered module fragment plans. The shared core is always prepended.
_MODULE_PLAN: dict[str, tuple[str, ...]] = {
    "CORE": (),
    "interactive": ("modules/ui-a", "modules/ui-physics", "modules/ui-b", "modules/palette"),
    "mockup": ("modules/ui-a", "modules/ui-b", "modules/palette"),
    "chart": ("modules/ui-a", "modules/ui-b", "modules/palette", "modules/chartjs"),
    "chart_interactive": ("modules/ui-a", "modules/ui-b", "modules/palette", "modules/chartjs"),
    "art": ("modules/budget", "modules/svg-core", "modules/art"),
    "art_interactive": (
        "modules/budget",
        "modules/svg-core",
        "modules/art",
        "modules/ui-a",
        "modules/ui-physics",
        "modules/ui-b",
        "modules/palette",
    ),
    "diagram": ("modules/palette", "modules/budget", "modules/svg-core", "modules/diagram-types"),
}


def available_modules() -> tuple[str, ...]:
    return tuple(name for name in _MODULE_PLAN if name != "CORE")


@lru_cache(maxsize=None)
def _read_fragment(rel_name: str) -> str:
    path = _FRAGMENTS_DIR / f"{rel_name}.md"
    return path.read_text(encoding="utf-8").strip()


@lru_cache(maxsize=None)
def compose_core() -> str:
    parts = (
        _read_fragment("core/00-head"),
        render_directions_block(),
        _read_fragment("core/20-direction-rules"),
        _read_fragment("core/30-craft"),
        _read_fragment("core/40-technical"),
    )
    return "\n\n".join(part.strip() for part in parts)


@lru_cache(maxsize=None)
def compose_bundle(widget_type: str) -> str:
    """Full guideline document for a widget type (or the bare core for "CORE"/unknown)."""
    plan = _MODULE_PLAN.get(widget_type, ())
    parts = [compose_core()]
    parts.extend(_read_fragment(rel) for rel in plan)
    return "\n\n".join(part.strip() for part in parts)


@lru_cache(maxsize=None)
def planning_layout_rules() -> str:
    return _read_fragment("planning/layout-rules")


@lru_cache(maxsize=None)
def example_widget_code() -> str:
    path = _FRAGMENTS_DIR / "examples" / "lab-dark-pendulum.html"
    return path.read_text(encoding="utf-8").strip()


def write_generated() -> list[Path]:
    """Regenerate the top-level guidelines/<module>.md artifacts from fragments."""
    written: list[Path] = []
    for name in _MODULE_PLAN:
        path = _GUIDELINES_DIR / f"{name}.md"
        path.write_text(_GENERATED_HEADER + compose_bundle(name) + "\n", encoding="utf-8")
        written.append(path)
    return written


if __name__ == "__main__":
    for path in write_generated():
        print(f"wrote {path}")
