"""Load skill definitions from SKILL.md files and build system prompts."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger("genui.skills")


@dataclass(frozen=True)
class SkillDefinition:
    name: str
    description: str
    guidance: str
    always: bool = True


def load_skills(skills_dir: Path) -> list[SkillDefinition]:
    skills: list[SkillDefinition] = []
    if not skills_dir.is_dir():
        return skills
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        skill = _parse_skill_md(skill_file)
        if skill:
            skills.append(skill)
            logger.info("loaded skill: %s", skill.name)
    return skills


def build_system_prompt(skills: list[SkillDefinition]) -> str:
    base = (
        "You are a visualization-focused assistant. "
        "Use tools only when the user explicitly asks for visual output, "
        "charts, diagrams, mockups, art, widgets, or simulations. "
        "For normal Q&A, respond with plain text and do not call tools. "
        "For visual output, follow strict tool order: visualize_read_me before show_widget. "
        "Follow the skill rules below.\n"
    )
    parts = ["<skills>"]
    for skill in skills:
        parts.append(
            f'<skill name="{skill.name}" always="{str(skill.always).lower()}">'
            f"<description>{skill.description}</description>"
            f"<guidance>{skill.guidance}</guidance>"
            f"</skill>"
        )
    parts.append("</skills>")
    return base + "".join(parts)


def _parse_skill_md(path: Path) -> SkillDefinition | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        logger.error("failed to read skill file %s: %s", path, exc)
        return None

    frontmatter, body = _split_frontmatter(text)
    name = frontmatter.get("name", path.parent.name)
    description = frontmatter.get("description", "")
    always = frontmatter.get("always", "true").lower() in ("true", "1", "yes")
    guidance = body.strip()

    if not name:
        return None
    return SkillDefinition(
        name=name, description=description, guidance=guidance, always=always
    )


def _split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    stripped = text.strip()
    if not stripped.startswith("---"):
        return {}, text

    end_idx = stripped.find("---", 3)
    if end_idx == -1:
        return {}, text

    fm_block = stripped[3:end_idx].strip()
    body = stripped[end_idx + 3:]

    props: dict[str, str] = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        props[key.strip()] = value.strip()
    return props, body
