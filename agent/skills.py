from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentSkill:
    name: str
    description: str
    guidance: str
    always: bool = True


class SkillsManager:
    def __init__(self, skills: list[AgentSkill]) -> None:
        self.skills = skills

    @classmethod
    def default(cls) -> "SkillsManager":
        return cls(
            [
                AgentSkill(
                    name="generative_ui",
                    description="Route visualization requests to read_me and show_widget tools.",
                    guidance=(
                        "For visual requests, call visualize_read_me first, then show_widget. "
                        "Use English tool labels and one widget_type from interactive/chart/mockup/art/diagram."
                    ),
                    always=True,
                )
            ]
        )

    def summary_xml(self) -> str:
        parts: list[str] = ["<skills>"]
        for skill in self.skills:
            parts.append(
                f'<skill name="{skill.name}" always="{str(skill.always).lower()}">'
                f"<description>{skill.description}</description>"
                f"<guidance>{skill.guidance}</guidance>"
                f"</skill>"
            )
        parts.append("</skills>")
        return "".join(parts)

    def build_system_prompt(self) -> str:
        return (
            "You are a visualization-focused assistant. "
            "Use tools only when the user explicitly asks for visual output, charts, diagrams, mockups, art, widgets, or simulations. "
            "For normal Q&A, respond with plain text and do not call tools. "
            "Follow the skill rules below.\n"
            f"{self.summary_xml()}"
        )
