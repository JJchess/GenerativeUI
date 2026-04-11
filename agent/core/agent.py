"""Agent control loop: LLM reasoning, tool execution, event streaming.

This module contains the generic agent loop that:
1. Sends messages to the LLM provider
2. Handles tool calls via the ToolRegistry
3. Delegates flow-control decisions to a SkillOrchestrator
4. Yields SSE-style events for the HTTP layer
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from typing import Any, Generator

from agent.core.config import AgentConfig
from agent.providers.geminiProviders import GeminiProvider
from agent.skills.generative_ui.orchestrator import GenerativeUIOrchestrator
from agent.tools.registry import ToolRegistry

logger = logging.getLogger("genui.agent")

MAX_TURNS = 5


class AgentLoop:
    def __init__(
        self,
        config: AgentConfig,
        tool_registry: ToolRegistry,
        orchestrator: GenerativeUIOrchestrator,
    ) -> None:
        self.config = config
        self.tools = tool_registry
        self.orchestrator = orchestrator

    def stream(
        self,
        messages: list[dict[str, Any]],
        user_text: str,
    ) -> Generator[dict[str, Any], None, str]:
        self.orchestrator.on_turn_start(user_text)

        provider = GeminiProvider(
            api_key=self.config.api_key,
            default_model=self.config.model,
        )
        tool_defs = self.tools.get_definitions()
        collected: list[str] = []

        for _ in range(MAX_TURNS):
            tool_choice = self.orchestrator.get_tool_choice()

            response = asyncio.run(
                provider.chat(
                    messages=messages,
                    tools=tool_defs,
                    model=self.config.model,
                    temperature=0.3,
                    max_tokens=4096,
                    tool_choice=tool_choice,
                )
            )
            logger.warning(
                "provider response finish_reason=%s has_tool_calls=%s content_len=%s",
                response.finish_reason,
                bool(response.tool_calls),
                len(response.content or ""),
            )

            if response.finish_reason == "error":
                fallback = response.content or response.error or "LLM error"
                logger.error("provider error -> %s", fallback)
                safe_text = "模型服务暂时不稳定，请重试。若持续失败，请检查网络或稍后再试。"
                yield from _emit_text(safe_text, collected)
                return "".join(collected)

            assistant_content = response.content or ""

            if not response.tool_calls:
                directive = self.orchestrator.on_no_tool_calls(
                    assistant_content, response.provider_specific_fields
                )
                if directive.action == "retry":
                    messages.extend(directive.inject_messages)
                    continue
                if assistant_content:
                    yield from _emit_text(assistant_content, collected)
                return "".join(collected)

            if assistant_content:
                yield from _emit_text(assistant_content, collected)

            messages.append({
                "role": "assistant",
                "content": assistant_content or None,
                "tool_calls": [c.to_openai_tool_call() for c in response.tool_calls],
                "provider_specific_fields": response.provider_specific_fields,
            })

            for tool_call in response.tool_calls:
                logger.warning("tool call name=%s id=%s", tool_call.name, tool_call.id)

                directive = self.orchestrator.before_tool_call(tool_call)
                if directive.action == "skip":
                    messages.extend(directive.inject_messages)
                    continue

                tool_call_id = tool_call.id or str(uuid.uuid4())
                arguments = self.orchestrator.enrich_tool_arguments(
                    tool_call.name, dict(tool_call.arguments), user_text
                )

                execution = self.tools.execute(tool_call.name, arguments, tool_call_id)
                logger.warning(
                    "tool execution name=%s events=%s content_len=%s",
                    tool_call.name,
                    len(execution.events),
                    len(execution.content or ""),
                )

                post = self.orchestrator.after_tool_execution(
                    tool_call.name, execution.content
                )
                if post.action == "skip":
                    messages.extend(post.inject_messages)
                    continue

                self.orchestrator.on_tool_events_emitted(
                    tool_call.name, bool(execution.events)
                )

                for event in execution.events:
                    yield event
                    if event.get("type") == "toolcall_delta":
                        time.sleep(0.03)

                messages.append({
                    "role": "tool",
                    "name": tool_call.name,
                    "content": execution.content,
                })

        fallback = self.orchestrator.get_fallback_text()
        if fallback:
            yield from _emit_text(fallback, collected)
        return "".join(collected)


def _emit_text(
    text: str,
    collector: list[str],
    delay: float = 0.008,
) -> Generator[dict[str, Any], None, None]:
    if not text:
        return
    for token in text:
        collector.append(token)
        yield {"type": "assistant_delta", "delta": token}
        if delay > 0:
            time.sleep(delay)
