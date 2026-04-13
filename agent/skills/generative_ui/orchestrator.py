"""Orchestrator for the generative_ui skill: visual flow state machine.

Encapsulates the guardrail logic that ensures visualize_read_me is called
before show_widget, prevents duplicate widgets, and injects corrective
turns when the model deviates from the expected tool-call sequence.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Literal

from agent.skills.generative_ui.visual_triggers import VISUAL_TRIGGERS_EN, VISUAL_TRIGGERS_ZH

logger = logging.getLogger("genui.orchestrator.generative_ui")

# After this many successful visualize_read_me calls, require show_widget only (avoids endless read_me).
MAX_READ_ME_SUCCESS_ROUNDS_BEFORE_FORCE_WIDGET = 3


@dataclass
class VisualFlowState:
    visual_request: bool = False
    visual_flow_started: bool = False
    show_widget_emitted: bool = False
    has_loaded_guidelines: bool = False
    read_me_success_rounds: int = 0
    # Host-injected read_me trailer (few-shot + "next action") at most once per user turn.
    read_me_trailer_emitted: bool = False


@dataclass
class Directive:
    action: Literal["proceed", "skip", "retry"]
    inject_messages: list[dict[str, Any]] = field(default_factory=list)


class GenerativeUIOrchestrator:

    def __init__(self) -> None:
        self.state = VisualFlowState()

    def on_turn_start(self, user_text: str) -> None:
        self.state = VisualFlowState(
            visual_request=self._is_visual_request(user_text),
        )

    def get_tool_choice(self) -> str | dict[str, Any]:
        # First hop: require a tool so the model loads guidelines (not prose-only).
        if self.state.visual_request and not self.state.has_loaded_guidelines:
            logger.info("tool_choice=required (visual_request, guidelines not loaded)")
            return "required"
        # Allow more visualize_read_me calls (other modules) without truncating payloads.
        if (
            self.state.visual_request
            and self.state.has_loaded_guidelines
            and not self.state.show_widget_emitted
            and self.state.read_me_success_rounds < MAX_READ_ME_SUCCESS_ROUNDS_BEFORE_FORCE_WIDGET
        ):
            logger.info(
                "tool_choice=required (read_me rounds=%s/%s or show_widget)",
                self.state.read_me_success_rounds,
                MAX_READ_ME_SUCCESS_ROUNDS_BEFORE_FORCE_WIDGET,
            )
            return "required"
        if (
            self.state.visual_request
            and self.state.has_loaded_guidelines
            and not self.state.show_widget_emitted
        ):
            logger.info("tool_choice=forced show_widget (read_me cap reached, widget pending)")
            return {"type": "function", "function": {"name": "show_widget"}}
        logger.info("tool_choice=auto")
        return "auto"

    def on_no_tool_calls(
        self,
        assistant_content: str,
        provider_specific_fields: dict[str, Any] | None,
    ) -> Directive:
        if (
            (self.state.visual_request or self.state.visual_flow_started)
            and not self.state.show_widget_emitted
        ):
            logger.warning("visual request received no tool calls, injecting corrective turn")
            return Directive(
                action="retry",
                inject_messages=[
                    {
                        "role": "assistant",
                        "content": assistant_content or None,
                        "provider_specific_fields": provider_specific_fields,
                    },
                    {
                        "role": "user",
                        "content": (
                            "Last turn had no tool_calls while tools are mandatory. "
                            "Follow the generative_ui skill: if read_me output is already in messages, "
                            "call show_widget with i_have_seen_read_me=true; otherwise call "
                            "visualize_read_me then show_widget. Do not use prose-only."
                        ),
                    },
                ],
            )
        return Directive(action="proceed")

    def before_tool_call(self, tool_call: Any) -> Directive:
        if tool_call.name == "visualize_read_me":
            self.state.visual_flow_started = True
            self.state.has_loaded_guidelines = True

        if tool_call.name == "show_widget" and not self.state.has_loaded_guidelines:
            logger.warning("show_widget blocked: visualize_read_me not called yet")
            return Directive(
                action="skip",
                inject_messages=[
                    {"role": "tool", "name": "show_widget", "content": "READ_ME_REQUIRED"},
                    {
                        "role": "user",
                        "content": (
                            "Follow the generative_ui skill: call visualize_read_me with relevant "
                            "modules before show_widget; then retry show_widget with i_have_seen_read_me=true."
                        ),
                    },
                ],
            )

        if tool_call.name == "show_widget" and self.state.show_widget_emitted:
            logger.warning("duplicate show_widget skipped after first successful render")
            return Directive(
                action="skip",
                inject_messages=[
                    {"role": "tool", "name": "show_widget", "content": "SHOW_WIDGET_ALREADY_EMITTED"},
                    {
                        "role": "user",
                        "content": (
                            "Per generative_ui skill: do not call show_widget again; continue with plain assistant text."
                        ),
                    },
                ],
            )

        return Directive(action="proceed")

    def after_tool_execution(self, tool_name: str, result_content: str) -> Directive:
        if tool_name == "visualize_read_me" and result_content and "No guidelines found" not in str(
            result_content
        ):
            self.state.read_me_success_rounds += 1

        if tool_name == "show_widget" and result_content == "READ_ME_REQUIRED":
            logger.warning("show_widget rejected: READ_ME_REQUIRED")
            return Directive(
                action="skip",
                inject_messages=[
                    {"role": "tool", "name": tool_name, "content": "READ_ME_REQUIRED"},
                    {
                        "role": "user",
                        "content": (
                            "Follow the generative_ui skill: visualize_read_me first, then show_widget "
                            "with i_have_seen_read_me=true."
                        ),
                    },
                ],
            )

        if tool_name == "show_widget" and result_content == "INVALID_WIDGET_CODE":
            logger.warning("invalid widget code detected, requesting regeneration")
            return Directive(
                action="skip",
                inject_messages=[
                    {"role": "tool", "name": tool_name, "content": "INVALID_WIDGET_CODE"},
                    {
                        "role": "user",
                        "content": (
                            "show_widget was rejected (INVALID_WIDGET_CODE). Regenerate per generative_ui skill "
                            "and tool schema: complete fragment with <style>, interactive markup, and <script>."
                        ),
                    },
                ],
            )

        return Directive(action="proceed")

    def on_tool_events_emitted(self, tool_name: str, has_events: bool) -> None:
        if tool_name == "show_widget" and has_events:
            self.state.show_widget_emitted = True

    def get_fallback_text(self, lang: str = "zh") -> str | None:
        if self.state.visual_request and not self.state.show_widget_emitted:
            messages = {
                "zh": "本次可视化生成未能输出组件，请重试，或补充需求细节（数据结构、交互方式、配色）。",
                "en": "Visualization generation failed to produce a widget. Please retry or add more detail (data structure, interactions, color scheme).",
            }
            return messages.get(lang, messages["en"])
        return None

    def enrich_tool_arguments(
        self, tool_name: str, arguments: dict[str, Any], user_text: str
    ) -> dict[str, Any]:
        if tool_name != "show_widget":
            return arguments
        enriched = dict(arguments)
        if "i_have_seen_read_me" not in enriched:
            enriched["i_have_seen_read_me"] = self.state.has_loaded_guidelines
        elif bool(enriched.get("i_have_seen_read_me")) != bool(self.state.has_loaded_guidelines):
            logger.warning(
                "i_have_seen_read_me mismatch: model=%s state=%s",
                enriched.get("i_have_seen_read_me"),
                self.state.has_loaded_guidelines,
            )
        enriched.setdefault("loading_messages", self._default_loading_messages(user_text))
        return enriched

    @staticmethod
    def _is_visual_request(user_text: str) -> bool:
        normalized = user_text.lower()
        if any(t in normalized for t in VISUAL_TRIGGERS_EN):
            return True
        return any(t in user_text for t in VISUAL_TRIGGERS_ZH)

    @staticmethod
    def _default_loading_messages(user_text: str) -> list[str]:
        normalized = user_text.lower()
        if any(t in normalized for t in ["chart", "graph", "plot", "histogram", "timeseries"]):
            return ["Preparing chart structure", "Binding chart data", "Rendering chart interactions"]
        if any(t in normalized for t in ["diagram", "architecture", "flow", "workflow"]):
            return ["Preparing diagram layout", "Routing connectors", "Rendering final diagram"]
        if any(t in normalized for t in ["mockup", "form", "layout", "ui"]):
            return ["Preparing mockup layout", "Applying component styles", "Rendering UI interactions"]
        if any(t in normalized for t in ["art", "illustration", "draw", "creative"]):
            return ["Preparing art composition", "Applying visual layers", "Rendering final illustration"]
        return ["Preparing interactive layout", "Binding controls", "Rendering interactive widget"]
