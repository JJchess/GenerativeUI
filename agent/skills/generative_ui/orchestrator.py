"""Orchestrator for the generative_ui skill: visual flow state machine.

Encapsulates the guardrail logic that ensures visualize_read_me is called
before show_widget, prevents duplicate widgets, and injects corrective
turns when the model deviates from the expected tool-call sequence.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Literal

logger = logging.getLogger("genui.orchestrator.generative_ui")

VISUAL_TRIGGERS = [
    "visual", "widget", "chart", "diagram", "interactive",
    "simulation", "dashboard", "graph",
]


@dataclass
class VisualFlowState:
    visual_request: bool = False
    visual_flow_started: bool = False
    show_widget_emitted: bool = False
    has_loaded_guidelines: bool = False


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

    def get_tool_choice(self) -> str:
        if self.state.visual_request and not self.state.has_loaded_guidelines:
            return "required"
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
                            "You must call visualize_read_me and then show_widget "
                            "for this request. Do not answer with prose only."
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
                            "Before show_widget, call visualize_read_me with relevant "
                            "modules, then retry show_widget with i_have_seen_read_me=true."
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
                        "content": "Do not call show_widget again in this turn. Continue with plain assistant text only.",
                    },
                ],
            )

        return Directive(action="proceed")

    def after_tool_execution(self, tool_name: str, result_content: str) -> Directive:
        if tool_name == "show_widget" and result_content == "READ_ME_REQUIRED":
            logger.warning("show_widget rejected: READ_ME_REQUIRED")
            return Directive(
                action="skip",
                inject_messages=[
                    {"role": "tool", "name": tool_name, "content": "READ_ME_REQUIRED"},
                    {
                        "role": "user",
                        "content": "Call visualize_read_me first and retry show_widget with i_have_seen_read_me=true.",
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
                        "content": "Regenerate show_widget with complete interactive HTML including script and controls.",
                    },
                ],
            )

        return Directive(action="proceed")

    def on_tool_events_emitted(self, tool_name: str, has_events: bool) -> None:
        if tool_name == "show_widget" and has_events:
            self.state.show_widget_emitted = True

    def get_fallback_text(self) -> str | None:
        if self.state.visual_request and not self.state.show_widget_emitted:
            return "本次可视化生成未成功输出组件，我已记录日志。请重试一次，或把需求再具体一些（数据结构、交互方式、配色）。"
        return None

    def enrich_tool_arguments(
        self, tool_name: str, arguments: dict[str, Any], user_text: str
    ) -> dict[str, Any]:
        if tool_name != "show_widget":
            return arguments
        enriched = dict(arguments)
        enriched.setdefault("i_have_seen_read_me", self.state.has_loaded_guidelines)
        enriched.setdefault("loading_messages", self._default_loading_messages(user_text))
        return enriched

    @staticmethod
    def _is_visual_request(user_text: str) -> bool:
        normalized = user_text.lower()
        return any(t in normalized for t in VISUAL_TRIGGERS)

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
