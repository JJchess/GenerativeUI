"""Agent control loop: LLM reasoning, tool execution, event streaming.

This module contains the generic agent loop that:
1. Streams text from the LLM provider in real-time
2. Handles tool calls via the ToolRegistry
3. Delegates flow-control decisions to a SkillOrchestrator
4. Yields SSE-style events for the HTTP layer
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from typing import Any, Generator

from agent.core.config import AgentConfig
from agent.providers.base import LLMResponse
from agent.providers.geminiProviders import GeminiProvider
from agent.skills.generative_ui.orchestrator import GenerativeUIOrchestrator
from agent.tools.registry import ToolRegistry

logger = logging.getLogger("genui.agent")

MAX_TURNS = 8


def _filter_redundant_post_widget_read_me(
    tool_calls: list[Any],
    *,
    has_loaded_guidelines: bool,
) -> list[Any]:
    """Drop visualize_read_me calls that appear after show_widget in the same model turn.

    Some models emit show_widget first then an extra visualize_read_me; executing the
    latter only burns tokens after guidelines are already in context.
    """
    if not has_loaded_guidelines or not tool_calls:
        return tool_calls
    last_show = -1
    for i, tc in enumerate(tool_calls):
        if getattr(tc, "name", None) == "show_widget":
            last_show = i
    if last_show < 0:
        return tool_calls
    out: list[Any] = []
    trimmed = False
    for i, tc in enumerate(tool_calls):
        if getattr(tc, "name", None) == "visualize_read_me" and i > last_show:
            trimmed = True
            continue
        out.append(tc)
    if trimmed:
        logger.info(
            "skipped visualize_read_me after show_widget in same batch (last show_widget index=%s)",
            last_show,
        )
    return out


def _log_model_response_complete(response: LLMResponse, assistant_text: str) -> None:
    """Log one JSON blob per model round: full text, tool args, usage, raw Gemini parts."""
    psf = response.provider_specific_fields if isinstance(response.provider_specific_fields, dict) else None
    raw_parts = psf.get("assistant_parts") if psf else None
    payload: dict[str, Any] = {
        "finish_reason": response.finish_reason,
        "usage": response.usage,
        "error": response.error,
        "text": assistant_text,
        "text_from_provider": response.content,
        "tool_calls": [
            {
                "id": tc.id,
                "name": tc.name,
                "arguments": tc.arguments,
                "provider_specific_fields": tc.provider_specific_fields,
            }
            for tc in response.tool_calls
        ],
        "raw_assistant_parts": raw_parts,
    }
    try:
        line = json.dumps(payload, ensure_ascii=False, default=str)
    except TypeError:
        line = json.dumps(
            {k: repr(v)[:50000] for k, v in payload.items()},
            ensure_ascii=False,
            default=str,
        )
    flag = os.getenv("GENUI_LOG_MODEL_FULL", "").strip().lower()
    if flag in ("1", "true", "yes", "on"):
        logger.info("model_output_full json=%s", line)
    else:
        logger.debug("model_output_full json=%s", line)


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
            logger.info("agent turn tool_choice=%s", tool_choice)

            turn_text: list[str] = []
            response: LLMResponse | None = None

            for event in provider.chat_stream_sync(
                messages=messages,
                tools=tool_defs,
                model=self.config.model,
                max_tokens=8192,
                temperature=0.3,
                tool_choice=tool_choice,
            ):
                if event.type == "text_delta" and event.delta:
                    turn_text.append(event.delta)
                    collected.append(event.delta)
                    yield {"type": "assistant_delta", "delta": event.delta}
                elif event.type == "response":
                    response = event.response

            if response is None:
                return "".join(collected)

            streamed = "".join(turn_text)
            resp_text = (response.content or "").strip()
            if resp_text and not streamed.strip():
                delta = response.content or ""
                turn_text.append(delta)
                collected.append(delta)
                yield {"type": "assistant_delta", "delta": delta}

            assistant_content = "".join(turn_text) or response.content or ""

            _log_model_response_complete(response, assistant_content)
            logger.info(
                "provider response finish_reason=%s has_tool_calls=%s content_len=%s",
                response.finish_reason,
                bool(response.tool_calls),
                len(assistant_content),
            )

            if response.finish_reason == "error":
                logger.error("provider error -> %s", response.content or response.error)
                safe_text = "模型服务暂时不稳定，请重试。若持续失败，请检查网络或稍后再试。"
                yield from _emit_system_text(safe_text, collected)
                return "".join(collected)

            if not response.tool_calls:
                directive = self.orchestrator.on_no_tool_calls(
                    assistant_content, response.provider_specific_fields
                )
                if directive.action == "retry":
                    messages.extend(directive.inject_messages)
                    continue
                return "".join(collected)

            calls = _filter_redundant_post_widget_read_me(
                response.tool_calls,
                has_loaded_guidelines=self.orchestrator.state.has_loaded_guidelines,
            )
            provider_fields = response.provider_specific_fields
            if len(calls) < len(response.tool_calls) and isinstance(provider_fields, dict):
                # Drop raw Gemini parts so replay matches the filtered tool_calls list.
                provider_fields = {k: v for k, v in provider_fields.items() if k != "assistant_parts"}

            messages.append({
                "role": "assistant",
                "content": assistant_content or None,
                "tool_calls": [c.to_openai_tool_call() for c in calls],
                "provider_specific_fields": provider_fields,
            })

            for tool_call in calls:
                logger.info("tool call name=%s id=%s", tool_call.name, tool_call.id)

                directive = self.orchestrator.before_tool_call(tool_call)
                if directive.action == "skip":
                    messages.extend(directive.inject_messages)
                    continue

                tool_call_id = tool_call.id or str(uuid.uuid4())
                arguments = self.orchestrator.enrich_tool_arguments(
                    tool_call.name, dict(tool_call.arguments), user_text
                )

                attach_read_me_trailer: bool | None = None
                if tool_call.name == "visualize_read_me":
                    attach_read_me_trailer = not self.orchestrator.state.read_me_trailer_emitted

                execution = self.tools.execute(
                    tool_call.name,
                    arguments,
                    tool_call_id,
                    attach_read_me_trailer=attach_read_me_trailer,
                )
                logger.info(
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

                for evt in execution.events:
                    yield evt

                messages.append({
                    "role": "tool",
                    "name": tool_call.name,
                    "content": execution.content,
                })
                if (
                    tool_call.name == "visualize_read_me"
                    and execution.content
                    and "No guidelines found" not in str(execution.content)
                    and attach_read_me_trailer is True
                ):
                    self.orchestrator.state.read_me_trailer_emitted = True

        fallback = self.orchestrator.get_fallback_text()
        if fallback:
            yield from _emit_system_text(fallback, collected)
        return "".join(collected)


def _emit_system_text(
    text: str,
    collector: list[str],
) -> Generator[dict[str, Any], None, None]:
    """Emit system-generated text (errors, fallbacks). Not model output."""
    if not text:
        return
    collector.append(text)
    yield {"type": "assistant_delta", "delta": text}
