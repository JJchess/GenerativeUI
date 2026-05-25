"""Orchestrator for the generative_ui skill."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from agent.skills.generative_ui.visual_triggers import VISUAL_TRIGGERS_EN, VISUAL_TRIGGERS_ZH


@dataclass
class VisualFlowState:
    visual_request: bool = False
    widget_emitted: bool = False
    attempted_generation: bool = False


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
        if self.state.visual_request and not self.state.widget_emitted:
            return "required"
        return "auto"

    def on_no_tool_calls(
        self,
        assistant_content: str,
        provider_specific_fields: dict[str, Any] | None,
    ) -> Directive:
        if (
            self.state.visual_request
            and not self.state.widget_emitted
        ):
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
                            "Last turn had no tool_calls while a visual widget is required. "
                            "Call generative_ui with the current request as query and do not answer with prose only."
                        ),
                    },
                ],
            )
        return Directive(action="proceed")

    def before_tool_call(self, tool_call: Any) -> Directive:
        if tool_call.name == "generative_ui" and self.state.widget_emitted:
            return Directive(
                action="skip",
                inject_messages=[
                    {"role": "tool", "name": "generative_ui", "content": '{"status":"skipped","reason":"widget already emitted"}'},
                    {
                        "role": "user",
                        "content": (
                            "Per the generative_ui skill, do not call generative_ui again in this turn. Continue with plain assistant text."
                        ),
                    },
                ],
            )

        return Directive(action="proceed")

    def after_tool_execution(self, tool_name: str, result_content: str) -> Directive:
        if tool_name == "generative_ui":
            self.state.attempted_generation = True
        return Directive(action="proceed")

    def on_tool_events_emitted(self, tool_name: str, has_events: bool) -> None:
        if tool_name == "generative_ui" and has_events:
            self.state.widget_emitted = True

    def get_fallback_text(self, lang: str = "zh") -> str | None:
        if self.state.visual_request and not self.state.widget_emitted:
            messages = {
                "zh": "本次可视化生成未能输出组件，请重试，或补充需求细节（数据结构、交互方式、配色）。",
                "en": "Visualization generation failed to produce a widget. Please retry or add more detail (data structure, interactions, color scheme).",
            }
            return messages.get(lang, messages["en"])
        return None

    def enrich_tool_arguments(
        self, tool_name: str, arguments: dict[str, Any], user_text: str
    ) -> dict[str, Any]:
        if tool_name != "generative_ui":
            return arguments
        enriched = dict(arguments)
        enriched.setdefault("query", user_text)
        return enriched

    @staticmethod
    def _is_visual_request(user_text: str) -> bool:
        normalized = user_text.lower()
        if any(t in normalized for t in VISUAL_TRIGGERS_EN):
            return True
        return any(t in user_text for t in VISUAL_TRIGGERS_ZH)

