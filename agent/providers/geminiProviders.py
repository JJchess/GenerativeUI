from __future__ import annotations

import asyncio
import json
import logging
import uuid
from typing import Any

from google import genai

from .base import LLMProvider, LLMResponse, ToolCallRequest

logger = logging.getLogger("genui.gemini")


class GeminiProvider(LLMProvider):
    def __init__(
        self,
        api_key: str,
        api_base: str | None = None,
        default_model: str = "gemini-2.5-pro",
    ):
        super().__init__(api_key=api_key, api_base=api_base)
        self.default_model = default_model

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tool_choice: str | dict[str, Any] | None = None,
    ) -> LLMResponse:
        return await asyncio.to_thread(
            self._chat_sync,
            messages=messages,
            tools=tools,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            tool_choice=tool_choice,
        )

    def _chat_sync(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None,
        model: str | None,
        max_tokens: int,
        temperature: float,
        tool_choice: str | dict[str, Any] | None,
    ) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(content=None, finish_reason="error", error="Missing GEMINI_API_KEY")

        try:
            client = genai.Client(api_key=self.api_key)
            config: dict[str, Any] = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            system_instruction = self._collect_system_instruction(messages)
            if system_instruction:
                config["system_instruction"] = system_instruction
            converted_tools = self._to_gemini_tools(tools or [])
            if converted_tools:
                config["tools"] = [{"function_declarations": converted_tools}]
                tool_config = self._to_gemini_tool_config(tool_choice)
                if tool_config:
                    config["tool_config"] = tool_config

            response = client.models.generate_content(
                model=model or self.default_model,
                contents=self._to_gemini_contents(messages),
                config=config,
            )
            body = self._response_to_dict(response)
        except Exception as exc:
            return LLMResponse(
                content=str(exc),
                finish_reason="error",
                error=str(exc),
            )

        return self._parse_gemini_response(body, retry_after=None)

    def _to_gemini_contents(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        contents: list[dict[str, Any]] = []

        for msg in messages:
            role = msg.get("role")
            if role == "system":
                continue

            if role == "tool":
                tool_name = msg.get("name") or "tool"
                tool_content = self._stringify_content(msg.get("content"))
                contents.append(
                    {
                        "role": "user",
                        "parts": [
                            {
                                "functionResponse": {
                                    "name": str(tool_name),
                                    "response": {"content": tool_content},
                                }
                            }
                        ],
                    }
                )
                continue

            if role == "assistant" and msg.get("tool_calls"):
                provider_fields = msg.get("provider_specific_fields")
                if isinstance(provider_fields, dict):
                    assistant_parts = provider_fields.get("assistant_parts")
                    if isinstance(assistant_parts, list) and assistant_parts:
                        contents.append({"role": "model", "parts": assistant_parts})
                        continue
                parts: list[dict[str, Any]] = []
                text_content = self._stringify_content(msg.get("content"))
                if text_content:
                    parts.append({"text": text_content})
                for call in msg.get("tool_calls", []):
                    fn = call.get("function", {})
                    name = fn.get("name")
                    arguments_raw = fn.get("arguments", "{}")
                    try:
                        arguments = json.loads(arguments_raw) if isinstance(arguments_raw, str) else arguments_raw
                    except Exception:
                        arguments = {}
                    if name:
                        function_call_payload: dict[str, Any] = {"name": str(name), "args": arguments or {}}
                        provider_fields = call.get("provider_specific_fields")
                        if isinstance(provider_fields, dict):
                            thought_signature = provider_fields.get("thought_signature") or provider_fields.get("thoughtSignature")
                            if isinstance(thought_signature, str) and thought_signature:
                                function_call_payload["thought_signature"] = thought_signature
                                function_call_payload["thoughtSignature"] = thought_signature
                        parts.append({"functionCall": function_call_payload})
                if parts:
                    contents.append({"role": "model", "parts": parts})
                continue

            gemini_role = "model" if role == "assistant" else "user"
            text = self._stringify_content(msg.get("content"))
            if text:
                contents.append({"role": gemini_role, "parts": [{"text": text}]})

        if not contents:
            contents.append({"role": "user", "parts": [{"text": "Hello"}]})

        return contents

    def _collect_system_instruction(self, messages: list[dict[str, Any]]) -> str | None:
        system_chunks: list[str] = []
        for msg in messages:
            if msg.get("role") == "system":
                text = self._stringify_content(msg.get("content"))
                if text:
                    system_chunks.append(text)
        if not system_chunks:
            return None
        return "\n\n".join(system_chunks)

    def _to_gemini_tools(self, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        declarations: list[dict[str, Any]] = []
        for tool in tools:
            function_payload = tool.get("function", tool)
            name = function_payload.get("name")
            if not name:
                continue
            declaration: dict[str, Any] = {
                "name": str(name),
                "description": str(function_payload.get("description", "")),
            }
            parameters = function_payload.get("parameters")
            if isinstance(parameters, dict):
                declaration["parameters"] = parameters
            declarations.append(declaration)
        return declarations

    def _to_gemini_tool_config(self, tool_choice: str | dict[str, Any] | None) -> dict[str, Any] | None:
        if tool_choice is None:
            return None
        if isinstance(tool_choice, str):
            mode = "AUTO"
            if tool_choice == "required":
                mode = "ANY"
            if tool_choice == "none":
                mode = "NONE"
            return {"function_calling_config": {"mode": mode}}
        if isinstance(tool_choice, dict):
            function_name = None
            if tool_choice.get("type") == "function":
                function_name = (tool_choice.get("function") or {}).get("name")
            if function_name:
                return {
                    "function_calling_config": {
                        "mode": "ANY",
                        "allowed_function_names": [str(function_name)],
                    }
                }
        return None

    def _parse_gemini_response(self, body: dict[str, Any], retry_after: float | None) -> LLMResponse:
        candidates = body.get("candidates") or []
        if not candidates:
            return LLMResponse(content=None, finish_reason="stop", usage=self._extract_usage(body), retry_after=retry_after)

        candidate = candidates[0]
        finish_reason = str(candidate.get("finishReason", "stop")).lower()
        content_payload = candidate.get("content") or {}
        parts = content_payload.get("parts") or []
        logger.warning("candidate parts_count=%s", len(parts) if isinstance(parts, list) else 0)

        text_chunks: list[str] = []
        tool_calls: list[ToolCallRequest] = []
        for part in parts:
            text = part.get("text") if isinstance(part, dict) else None
            if isinstance(text, str) and text:
                text_chunks.append(text)
            function_call = None
            if isinstance(part, dict):
                function_call = part.get("functionCall") or part.get("function_call")
            if isinstance(function_call, dict):
                logger.warning("function_call keys=%s", ",".join(sorted(function_call.keys())))
                function_name = function_call.get("name")
                if isinstance(function_name, str) and function_name:
                    args = function_call.get("args")
                    if not isinstance(args, dict):
                        args = {}
                    tool_calls.append(
                        ToolCallRequest(
                            id=str(uuid.uuid4()),
                            name=function_name,
                            arguments=args,
                            provider_specific_fields=self._extract_function_call_provider_fields(function_call),
                        )
                    )
                    logger.warning(
                        "parsed tool_call name=%s has_signature=%s",
                        function_name,
                        bool(tool_calls[-1].provider_specific_fields),
                    )
                    if function_name == "show_widget":
                        widget_code = args.get("widget_code")
                        widget_len = len(widget_code) if isinstance(widget_code, str) else 0
                        widget_preview = (widget_code[:180] if isinstance(widget_code, str) else "")
                        logger.warning(
                            "show_widget args title=%s widget_len=%s preview=%s",
                            str(args.get("title", ""))[:80],
                            widget_len,
                            widget_preview.replace("\n", "\\n"),
                        )

        usage = self._extract_usage(body)
        content = "\n".join(chunk for chunk in text_chunks if chunk.strip()) or None
        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            finish_reason=finish_reason,
            usage=usage,
            retry_after=retry_after,
            provider_specific_fields={"assistant_parts": parts},
        )

    def _extract_usage(self, body: dict[str, Any]) -> dict[str, int]:
        usage = body.get("usageMetadata") or body.get("usage_metadata") or {}
        result: dict[str, int] = {}
        if isinstance(usage.get("promptTokenCount"), int):
            result["prompt_tokens"] = usage["promptTokenCount"]
        elif isinstance(usage.get("prompt_token_count"), int):
            result["prompt_tokens"] = usage["prompt_token_count"]
        if isinstance(usage.get("candidatesTokenCount"), int):
            result["completion_tokens"] = usage["candidatesTokenCount"]
        elif isinstance(usage.get("candidates_token_count"), int):
            result["completion_tokens"] = usage["candidates_token_count"]
        if isinstance(usage.get("totalTokenCount"), int):
            result["total_tokens"] = usage["totalTokenCount"]
        elif isinstance(usage.get("total_token_count"), int):
            result["total_tokens"] = usage["total_token_count"]
        return result

    def _stringify_content(self, content: Any) -> str:
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            chunks: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        chunks.append(text)
                elif isinstance(item, str):
                    chunks.append(item)
            return "\n".join(chunk for chunk in chunks if chunk)
        return str(content)

    def _response_to_dict(self, response: Any) -> dict[str, Any]:
        try:
            if hasattr(response, "model_dump"):
                data = response.model_dump()
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        try:
            if hasattr(response, "to_dict"):
                data = response.to_dict()
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        try:
            text = str(response)
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass
        return {}

    def _extract_function_call_provider_fields(self, function_call: dict[str, Any]) -> dict[str, Any] | None:
        thought_signature = function_call.get("thought_signature") or function_call.get("thoughtSignature")
        if isinstance(thought_signature, str) and thought_signature:
            return {"thought_signature": thought_signature, "thoughtSignature": thought_signature}
        return None
