from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

from agent.core.config import resolve_config
from agent.providers.geminiProviders import GeminiProvider
from agent.tools.base import AgentTool, ToolExecutionResult

from .prompts import (
    build_planning_prompt,
    build_primary_prompt,
    build_repair_prompt,
    build_validation_repair_prompt,
    recent_conversation_context,
)
from .validators import (
    infer_widget_type,
    is_payload_usable,
    is_widget_code_valid,
    normalize_title,
    normalize_widget_type,
    parse_split_response,
    payload_validation_errors,
    safe_int,
    safe_loading_messages,
)


class GenerativeUITool(AgentTool):
    name = "generative_ui"
    description = (
        "Generate an interactive HTML widget or visual demo for the current discussion. "
        "Use when a role wants to show an explorable UI, diagram, chart, or simulation."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "query": {
                "type": "string",
                "description": "What UI, simulation, chart, or interactive visual should be generated.",
            },
            "reset_session": {
                "type": "boolean",
                "description": "Reserved for compatibility. Presently ignored by the backend.",
                "default": False,
            },
            "debug_trace": {
                "type": "boolean",
                "description": "Whether to append prompts and raw model responses to llm_debug.ndjson.",
                "default": True,
            },
        },
        "required": ["query"],
    }

    def execute(self, arguments: dict[str, Any], tool_call_id: str) -> ToolExecutionResult:
        resolved_query = str(
            arguments.get("query")
            or arguments.get("component")
            or arguments.get("description")
            or arguments.get("prompt")
            or ""
        ).strip()
        if not resolved_query:
            return self._error_result("GenerativeUI query is required")

        config = resolve_config()
        if not config.has_key or not config.api_key:
            return self._error_result("Missing GEMINI_API_KEY/GOOGLE_API_KEY for GenerativeUI")

        debug_trace = bool(arguments.get("debug_trace", True))
        debug_trace_enabled = self._debug_trace_enabled(debug_trace)
        debug_trace_id = self._new_debug_trace_id() if debug_trace_enabled else ""

        conversation_messages = arguments.get("_conversation_messages")
        recent_context = recent_conversation_context(
            conversation_messages if isinstance(conversation_messages, list) else []
        )

        try:
            result = self._generate_widget_payload(
                query=resolved_query,
                recent_context=recent_context,
                api_key=config.api_key,
                model=config.model,
                debug_trace_enabled=debug_trace_enabled,
                debug_trace_id=debug_trace_id,
            )
        except Exception as exc:
            return self._error_result(f"GenerativeUI failed: {exc}")

        widget_code = str(result.get("widget_code") or "").strip()
        if not is_widget_code_valid(widget_code):
            return self._error_result("GenerativeUI returned invalid widget code")

        title = normalize_title(str(result.get("title") or "generated_widget"))
        widget_type = normalize_widget_type(str(result.get("widget_type") or "interactive"))
        loading_messages = safe_loading_messages(result.get("loading_messages"), resolved_query)
        width = safe_int(result.get("width"), 780)
        height = safe_int(result.get("height"), 520)
        assistant_text = str(result.get("assistant_text") or "").strip()

        events = [
            {
                "type": "toolcall_start",
                "tool_call_id": tool_call_id,
                "name": self.name,
                "widget_type": widget_type,
                "title": title,
                "width": width,
                "height": height,
                "loading_messages": loading_messages,
            },
            {
                "type": "toolcall_end",
                "tool_call_id": tool_call_id,
                "widget_code": widget_code,
            },
        ]
        content = {
            "query": resolved_query,
            "status": "completed",
            "assistant_text": assistant_text,
            "summary": assistant_text,
            "widget_count": 1,
            "widget_type": widget_type,
            "title": title,
        }
        if debug_trace_enabled:
            content["debug_trace_id"] = debug_trace_id
            content["debug_trace_file"] = str(self._debug_trace_path())
        return ToolExecutionResult(content=json.dumps(content, ensure_ascii=False), events=events)

    def _generate_widget_payload(
        self,
        *,
        query: str,
        recent_context: str,
        api_key: str,
        model: str,
        debug_trace_enabled: bool,
        debug_trace_id: str,
    ) -> Dict[str, Any]:
        widget_type = infer_widget_type(query)

        plan = self._run_planning_stage(
            query=query,
            widget_type=widget_type,
            recent_context=recent_context,
            api_key=api_key,
            model=model,
            debug_trace_enabled=debug_trace_enabled,
            debug_trace_id=debug_trace_id,
        )

        primary_prompt = build_primary_prompt(
            query=query,
            widget_type=widget_type,
            recent_context=recent_context,
            plan=plan,
        )
        raw = self._ask_with_debug_trace(
            stage="build",
            prompt=primary_prompt,
            query=query,
            widget_type=widget_type,
            temperature=0.3,
            api_key=api_key,
            model=model,
            debug_trace_enabled=debug_trace_enabled,
            debug_trace_id=debug_trace_id,
        )
        data = parse_split_response(raw)
        if is_payload_usable(data):
            return data

        repair_prompt = build_repair_prompt(query=query, broken_payload=data)
        repaired_raw = self._ask_with_debug_trace(
            stage="repair",
            prompt=repair_prompt,
            query=query,
            widget_type=str(data.get("widget_type") or widget_type),
            temperature=0.2,
            api_key=api_key,
            model=model,
            debug_trace_enabled=debug_trace_enabled,
            debug_trace_id=debug_trace_id,
        )
        repaired = parse_split_response(repaired_raw)
        if is_payload_usable(repaired):
            return repaired

        candidate = repaired if repaired else data
        errors = payload_validation_errors(candidate, expected_widget_type=widget_type)

        for attempt_index in range(1, 3):
            validation_prompt = build_validation_repair_prompt(
                query=query,
                widget_type=widget_type,
                recent_context=recent_context,
                broken_payload=candidate,
                validation_errors=errors,
            )
            validation_repair_raw = self._ask_with_debug_trace(
                stage=f"validation_repair_{attempt_index}",
                prompt=validation_prompt,
                query=query,
                widget_type=widget_type,
                temperature=0.15,
                api_key=api_key,
                model=model,
                debug_trace_enabled=debug_trace_enabled,
                debug_trace_id=debug_trace_id,
            )
            candidate = parse_split_response(validation_repair_raw)
            if is_payload_usable(candidate):
                return candidate
            errors = payload_validation_errors(candidate, expected_widget_type=widget_type)

        joined_errors = "; ".join(errors) if errors else "unknown validation errors"
        raise ValueError(f"widget payload is invalid after repair: {joined_errors}")

    def _run_planning_stage(
        self,
        *,
        query: str,
        widget_type: str,
        recent_context: str,
        api_key: str,
        model: str,
        debug_trace_enabled: bool,
        debug_trace_id: str,
    ) -> str:
        prompt = build_planning_prompt(
            query=query,
            widget_type=widget_type,
            recent_context=recent_context,
        )
        try:
            raw = self._ask_with_debug_trace(
                stage="plan",
                prompt=prompt,
                query=query,
                widget_type=widget_type,
                temperature=0.6,
                api_key=api_key,
                model=model,
                debug_trace_enabled=debug_trace_enabled,
                debug_trace_id=debug_trace_id,
            )
        except Exception:
            return ""

        text = (raw or "").strip()
        if text.startswith("```"):
            import re as _re

            text = _re.sub(r"^```[a-zA-Z]*\n?", "", text).rstrip("`").strip()

        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            candidate = text[start : end + 1]
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict) and parsed:
                    return json.dumps(parsed, ensure_ascii=False, indent=2)
            except Exception:
                return candidate
        return text

    def _ask_with_debug_trace(
        self,
        *,
        stage: str,
        prompt: str,
        query: str,
        widget_type: str,
        temperature: float,
        api_key: str,
        model: str,
        debug_trace_enabled: bool,
        debug_trace_id: str,
    ) -> str:
        provider = GeminiProvider(api_key=api_key, default_model=model)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a widget code generator. Follow the two-part response format exactly: "
                    "first a JSON metadata object, then a <widget_code>...</widget_code> block with raw HTML/CSS/JS."
                ),
            },
            {"role": "user", "content": prompt},
        ]
        started_at = datetime.now(timezone.utc)
        started_perf = time.perf_counter()
        raw_response = ""
        error_message = ""

        try:
            response = provider._chat_sync(
                messages=messages,
                tools=None,
                model=model,
                max_tokens=8192,
                temperature=temperature,
                tool_choice=None,
            )
            if response.finish_reason == "error":
                raise ValueError(response.error or response.content or "provider error")
            raw_response = str(response.content or "").strip()
            if not raw_response:
                raise ValueError("empty model response")
            return raw_response
        except Exception as exc:
            error_message = str(exc)
            raise
        finally:
            if debug_trace_enabled:
                self._append_debug_trace_entry(
                    {
                        "timestamp": started_at.isoformat(),
                        "debug_trace_id": debug_trace_id,
                        "tool_name": self.name,
                        "stage": stage,
                        "query": query,
                        "widget_type": widget_type,
                        "model": model,
                        "temperature": temperature,
                        "duration_ms": int((time.perf_counter() - started_perf) * 1000),
                        "prompt": prompt,
                        "raw_response": raw_response,
                        "error": error_message or None,
                    }
                )

    def _error_result(self, message: str) -> ToolExecutionResult:
        return ToolExecutionResult(
            content=json.dumps({"status": "error", "message": message}, ensure_ascii=False),
            events=[],
        )

    @staticmethod
    def _debug_trace_path() -> Path:
        return Path(__file__).resolve().parent / "llm_debug.ndjson"

    @staticmethod
    def _new_debug_trace_id() -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        return f"genui_trace_{timestamp}_{uuid4().hex[:8]}"

    @staticmethod
    def _truthy_env(value: str) -> bool:
        return value.strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
    def _falsy_env(value: str) -> bool:
        return value.strip().lower() in {"0", "false", "no", "off"}

    def _debug_trace_enabled(self, debug_trace: bool) -> bool:
        env_value = str(os.getenv("GENERATIVE_UI_DEBUG_TRACE", "") or "").strip()
        if env_value:
            if self._truthy_env(env_value):
                return True
            if self._falsy_env(env_value):
                return False
        return debug_trace

    def _append_debug_trace_entry(self, entry: Dict[str, Any]) -> None:
        try:
            trace_path = self._debug_trace_path()
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            with trace_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            return
