"""Streaming response helpers for OTEL tracing.

Pure functions that parse SSE byte streams and accumulate CompletionChunk
deltas into a ChatCompletionResponse-shaped dict suitable for span enrichment.

TODO: supports chat and agent completion streaming endpoints. Evolutions will
be necessary to support other streaming endpoints (e.g. conversations).

NOTE: The SSE bytes are re-parsed here even though EventStream already
parsed them during iteration.
TracedResponse sits below EventStream and can only accumulate raw bytes; it
has no access to the decoded events. Hooking into EventStream could eliminate
this double-parse, but EventStream is Speakeasy-generated code.
"""

from typing import Any

from mistralai.client.models import CompletionChunk, UsageInfo


def parse_sse_chunks(raw_sse_bytes: bytes) -> list[CompletionChunk]:
    """Parse raw SSE bytes into a list of typed CompletionChunk models.

    Only CompletionChunk is handled.  If new SSE-streamed response types
    are added, parsing and typing here will need updating.
    """
    chunks: list[CompletionChunk] = []
    text = raw_sse_bytes.decode("utf-8", errors="replace")
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("data: "):
            continue
        payload = line[6:]
        if payload == "[DONE]":
            continue
        try:
            chunks.append(CompletionChunk.model_validate_json(payload))
        except Exception:
            continue
    return chunks


def accumulate_chunks_to_response_dict(
    chunks: list[CompletionChunk],
) -> dict[str, Any]:
    """Accumulate streaming CompletionChunk deltas into a ChatCompletionResponse-shaped dict."""
    response_id: str | None = None
    model: str | None = None
    usage: UsageInfo | None = None
    choices: dict[int, dict[str, Any]] = {}

    for chunk in chunks:
        response_id = response_id or chunk.id
        model = model or chunk.model
        usage = usage or chunk.usage

        for choice in chunk.choices:
            accumulated = choices.setdefault(
                choice.index,
                {
                    "message": {"role": "assistant", "content": ""},
                    "finish_reason": "",
                },
            )
            msg = accumulated["message"]
            delta = choice.delta
            if isinstance(delta.role, str):
                msg["role"] = delta.role
            if isinstance(delta.content, str) and delta.content:
                msg["content"] += delta.content
            if isinstance(choice.finish_reason, str):
                accumulated["finish_reason"] = choice.finish_reason
            if isinstance(delta.tool_calls, list):
                tc_list = msg.setdefault("tool_calls", [])
                for tc in delta.tool_calls:
                    tc_idx = tc.index if tc.index is not None else len(tc_list)
                    while len(tc_list) <= tc_idx:
                        tc_list.append(
                            {"id": None, "function": {"name": "", "arguments": ""}}
                        )
                    # ToolCall.id defaults to the string "null" (Speakeasy codegen quirk)
                    if tc.id is not None and tc.id != "null":
                        tc_list[tc_idx]["id"] = tc.id
                    if tc.function.name:
                        tc_list[tc_idx]["function"]["name"] += tc.function.name
                    if isinstance(tc.function.arguments, str) and tc.function.arguments:
                        tc_list[tc_idx]["function"]["arguments"] += (
                            tc.function.arguments
                        )

    result: dict[str, Any] = {
        "id": response_id,
        "model": model,
        "choices": [choices[idx] for idx in sorted(choices)],
    }
    if usage is not None:
        result["usage"] = usage.model_dump(mode="json", by_alias=True)
    return result
