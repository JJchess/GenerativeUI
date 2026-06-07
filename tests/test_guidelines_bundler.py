"""Guideline bundler conformance tests.

Run:  python -m tests.test_guidelines_bundler   (from backend/)
or:   pytest tests/test_guidelines_bundler.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.skills.generative_ui.bundler import (  # noqa: E402
    available_modules,
    compose_bundle,
    compose_core,
    example_widget_code,
    planning_layout_rules,
)
from agent.skills.generative_ui.constants import WIDGET_TYPES  # noqa: E402
from agent.skills.generative_ui.directions import DIRECTIONS, render_direction_menu  # noqa: E402
from agent.skills.generative_ui.prompts import build_planning_prompt, build_primary_prompt  # noqa: E402
from agent.skills.generative_ui.validators import payload_validation_errors  # noqa: E402


def test_modules_match_widget_types():
    assert set(available_modules()) == set(WIDGET_TYPES)


def test_core_structure_ordered():
    core = compose_core()
    sections = ["## Design philosophy", "## Aesthetic directions", "### Direction rules",
                "## Craft rules", "## Technical contract", "## When nothing fits"]
    positions = [core.find(s) for s in sections]
    assert all(p >= 0 for p in positions), [s for s, p in zip(sections, positions) if p < 0]
    assert positions == sorted(positions), "core sections out of order"


def test_directions_complete():
    assert len(DIRECTIONS) == 7
    core = compose_core()
    for d in DIRECTIONS.values():
        assert d.spec_block in core, d.key
    menu = render_direction_menu()
    for key in DIRECTIONS:
        assert f"- {key}:" in menu


def test_every_bundle_self_contained():
    for name in WIDGET_TYPES:
        bundle = compose_bundle(name)
        assert "## Aesthetic directions" in bundle, name
        assert "## Technical contract" in bundle, name
        assert "Seamless" not in bundle, name
        assert "#4fc3f7" not in bundle.lower(), name


def test_module_specific_content():
    assert "Chart.js" in compose_bundle("chart")
    assert "Chart.js" in compose_bundle("chart_interactive")
    assert "## Diagram types" in compose_bundle("diagram")
    assert "## Art and illustration" in compose_bundle("art")
    assert "Physical & electrolysis simulators" in compose_bundle("interactive")
    assert "Physical & electrolysis simulators" not in compose_bundle("mockup")
    assert "## SVG setup" in compose_bundle("diagram")


def test_layout_rules_in_both_stages():
    plan = build_planning_prompt(query="q", widget_type="interactive", recent_context="")
    build = build_primary_prompt(query="q", widget_type="interactive", recent_context="", plan="")
    assert "align-items: start" in plan and "align-items: start" in build
    assert planning_layout_rules() in plan


def test_planning_menu_generated():
    plan = build_planning_prompt(query="q", widget_type="interactive", recent_context="")
    assert render_direction_menu() in plan
    for field in ["aesthetic_direction", "direction_reason", "palette", "signature_detail"]:
        assert f'"{field}"' in plan, field


def test_example_passes_validators():
    code = example_widget_code()
    payload = {"title": "t", "widget_type": "interactive", "assistant_text": "x", "widget_code": code}
    assert payload_validation_errors(payload) == []


def _main() -> int:
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as exc:
                failures += 1
                print(f"FAIL {name}: {exc}")
    print("OK" if not failures else f"{failures} FAILURES")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_main())
