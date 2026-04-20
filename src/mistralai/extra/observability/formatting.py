"""Formatting helpers for converting Mistral API payloads to OTEL GenAI convention formats.

These are pure functions with no OTEL dependencies — they transform dicts to dicts
matching the GenAI semantic convention schemas for input/output messages and tool definitions.
The caller is responsible for the final JSON serialization (single json.dumps on the whole
collection) before setting span attributes.

Schemas:
- Input messages: https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-input-messages.json
- Output messages: https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-output-messages.json
- Tool definitions: https://github.com/Cirilla-zmh/semantic-conventions/blob/cc4d07e7e56b80e9aa5904a3d524c134699da37f/docs/gen-ai/gen-ai-tool-definitions.json
"""

from typing import Any


def _content_to_parts(content) -> list[dict]:
    """Convert Mistral message content to OTEL parts array.

    Mistral content is either a string or an array of content chunks.
    """
    if content is None:
        return []
    if isinstance(content, str):
        return [{"type": "text", "content": content}]
    # Content chunks array — map known Mistral types to OTEL part types
    parts = []
    for chunk in content:
        if isinstance(chunk, str):
            parts.append({"type": "text", "content": chunk})
        elif isinstance(chunk, dict):
            chunk_type = chunk.get("type", "")
            if chunk_type == "text":
                parts.append({"type": "text", "content": chunk.get("text", "")})
            elif chunk_type == "thinking":
                thinking = chunk.get("thinking", "")
                if isinstance(thinking, list):
                    text_parts = [
                        sub.get("text", "")
                        for sub in thinking
                        if isinstance(sub, dict) and sub.get("type") == "text"
                    ]
                    content_str = "\n".join(text_parts)
                else:  # Fallback
                    content_str = str(thinking)
                parts.append({"type": "reasoning", "content": content_str})
            elif chunk_type == "image_url":
                url = chunk.get("image_url", {})
                uri = url.get("url", "") if isinstance(url, dict) else str(url)
                parts.append({"type": "uri", "modality": "image", "uri": uri})
            else:
                # Catch-all for other content chunk types
                parts.append({"type": chunk_type})
    return parts


def _tool_calls_to_parts(tool_calls: list[dict] | None) -> list[dict]:
    """Convert Mistral tool_calls to OTEL ToolCallRequestPart entries."""
    if not tool_calls:
        return []
    parts = []
    for tc in tool_calls:
        func = tc.get("function", {}) or {}
        part: dict = {
            "type": "tool_call",
            "name": func.get("name", ""),
        }
        if (tc_id := tc.get("id")) is not None:
            part["id"] = tc_id
        if (arguments := func.get("arguments")) is not None:
            part["arguments"] = arguments
        parts.append(part)
    return parts


def format_input_message(message: dict[str, Any]) -> dict[str, Any]:
    """Format a single input message per the OTEL GenAI convention.

    Schema: https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-input-messages.json
    ChatMessage: {role (required), parts (required), name?}

    Conversation entry objects (e.g. function.result) don't carry a "role"
    field — they are detected via their "type" and mapped to the closest
    OTEL role.
    """
    entry_type = message.get("type")

    # Conversation entry: function.result → OTEL tool role
    if entry_type == "function.result":
        part: dict = {"type": "tool_call_response", "response": message.get("result")}
        if (tool_call_id := message.get("tool_call_id")) is not None:
            part["id"] = tool_call_id
        return {"role": "tool", "parts": [part]}

    # TODO: may need to handle other types for conversations (e.g. agent handoff)

    role = message.get("role", "unknown")
    parts: list[dict] = []

    if role == "tool":
        # Tool messages are responses to tool calls
        tool_part: dict = {
            "type": "tool_call_response",
            "response": message.get("content"),
        }
        if (tool_call_id := message.get("tool_call_id")) is not None:
            tool_part["id"] = tool_call_id
        parts.append(tool_part)
    else:
        parts.extend(_content_to_parts(message.get("content")))
        parts.extend(_tool_calls_to_parts(message.get("tool_calls")))

    return {"role": role, "parts": parts}


def format_output_message(choice: dict[str, Any]) -> dict[str, Any]:
    """Format a single output choice/message per the OTEL GenAI convention.

    Schema: https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-output-messages.json
    OutputMessage: {role (required), parts (required), finish_reason (required), name?}
    """
    message = choice.get("message", {}) or {}
    parts: list[dict] = []
    parts.extend(_content_to_parts(message.get("content")))
    parts.extend(_tool_calls_to_parts(message.get("tool_calls")))

    return {
        "role": message.get("role", "assistant"),
        "parts": parts,
        "finish_reason": choice.get("finish_reason", ""),
    }


def format_tool_definition(tool: dict[str, Any]) -> dict[str, Any] | None:
    """Flatten a Mistral tool definition to the OTEL GenAI convention schema.

    Mistral format:  {"type": "function", "function": {"name": ..., "description": ..., "parameters": ...}}
    OTEL format:     {"type": "function", "name": ..., "description": ..., "parameters": ...}

    Schema, still under review: https://github.com/Cirilla-zmh/semantic-conventions/blob/cc4d07e7e56b80e9aa5904a3d524c134699da37f/docs/gen-ai/gen-ai-tool-definitions.json
    """
    # Early exit conditions: only functions supported for now, and name is required
    type = tool.get("type", "function")
    func = tool.get("function")
    if not func:
        return None
    name = func.get("name")
    if not name:
        return None
    formatted: dict = {"type": type, "name": name}
    if (description := func.get("description")) is not None:
        formatted["description"] = description
    if (parameters := func.get("parameters")) is not None:
        formatted["parameters"] = parameters
    return formatted
