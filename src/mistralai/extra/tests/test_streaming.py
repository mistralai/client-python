"""Tests for streaming SSE parsing and chunk accumulation.

Unit tests for the pure functions in ``observability.streaming``, independent
of OTEL span management.
"""

import json
import unittest

from mistralai.client.models import (
    CompletionChunk,
    CompletionResponseStreamChoice,
    CompletionResponseStreamChoiceFinishReason,
    DeltaMessage,
    FunctionCall,
    ToolCall,
    UsageInfo,
)
from mistralai.extra.observability.streaming import (
    accumulate_chunks_to_response_dict,
    parse_sse_chunks,
)

_DEFAULT_ID = "id-1"
_DEFAULT_MODEL = "m"


def _single_choice_chunk(
    id: str = _DEFAULT_ID,
    model: str = _DEFAULT_MODEL,
    role: str | None = None,
    content: str | None = None,
    tool_calls: list[ToolCall] | None = None,
    finish_reason: CompletionResponseStreamChoiceFinishReason | None = None,
    object: str | None = None,
    created: int | None = None,
    usage: UsageInfo | None = None,
) -> CompletionChunk:
    return CompletionChunk(
        id=id,
        model=model,
        choices=[
            CompletionResponseStreamChoice(
                index=0,
                delta=DeltaMessage(role=role, content=content, tool_calls=tool_calls),
                finish_reason=finish_reason,
            )
        ],
        object=object,
        created=created,
        usage=usage,
    )


def _dump(model) -> dict:
    return model.model_dump(mode="json", by_alias=True)


def _to_sse(chunks: list[CompletionChunk], done: bool = True) -> bytes:
    """Build SSE bytes from CompletionChunk models."""
    lines = [f"data: {json.dumps(_dump(c))}" for c in chunks]
    if done:
        lines.append("data: [DONE]")
    return ("\n\n".join(lines) + "\n\n").encode()


class TestParseSseChunks(unittest.TestCase):
    def test_parses_valid_chunks(self):
        chunks = [
            _single_choice_chunk(content="hello"),
            _single_choice_chunk(content=" world", finish_reason="stop"),
        ]
        result = parse_sse_chunks(_to_sse(chunks))
        self.assertEqual(result, chunks)

    def test_skips_done_sentinel(self):
        chunk = _single_choice_chunk(content="hi", finish_reason="stop")
        result = parse_sse_chunks(_to_sse([chunk], done=True))
        self.assertEqual(result, [chunk])

    def test_skips_invalid_json(self):
        sse = b"data: {not valid json}\n\ndata: [DONE]\n\n"
        result = parse_sse_chunks(sse)
        self.assertEqual(result, [])

    def test_skips_non_data_lines(self):
        chunk = _single_choice_chunk(content="hi", finish_reason="stop")
        sse = b"event: message\n\n" + _to_sse([chunk])
        result = parse_sse_chunks(sse)
        self.assertEqual(result, [chunk])

    def test_empty_bytes(self):
        self.assertEqual(parse_sse_chunks(b""), [])


class TestAccumulateChunks(unittest.TestCase):
    def test_simple_content_concatenation(self):
        chunks = [
            _single_choice_chunk(role="assistant", content="Hello"),
            _single_choice_chunk(content=" world"),
            _single_choice_chunk(
                content="",
                finish_reason="stop",
                usage=UsageInfo(prompt_tokens=10, completion_tokens=5, total_tokens=15),
            ),
        ]
        result = accumulate_chunks_to_response_dict(chunks)

        self.assertDictEqual(
            result,
            {
                "id": _DEFAULT_ID,
                "model": _DEFAULT_MODEL,
                "choices": [
                    {
                        "message": {"role": "assistant", "content": "Hello world"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                },
            },
        )

    def test_tool_call_argument_accumulation(self):
        """Tool call arguments fragmented across multiple chunks."""
        chunks = [
            _single_choice_chunk(
                role="assistant",
                content="",
                tool_calls=[
                    ToolCall(
                        id="tc-1",
                        index=0,
                        function=FunctionCall(name="get_weather", arguments=""),
                    )
                ],
            ),
            _single_choice_chunk(
                tool_calls=[
                    ToolCall(
                        index=0, function=FunctionCall(name="", arguments='{"location"')
                    )
                ],
            ),
            _single_choice_chunk(
                tool_calls=[
                    ToolCall(
                        index=0, function=FunctionCall(name="", arguments=': "Paris"}')
                    )
                ],
                finish_reason="tool_calls",
            ),
        ]
        result = accumulate_chunks_to_response_dict(chunks)

        self.assertDictEqual(
            result,
            {
                "id": _DEFAULT_ID,
                "model": _DEFAULT_MODEL,
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": "tc-1",
                                    "function": {
                                        "name": "get_weather",
                                        "arguments": '{"location": "Paris"}',
                                    },
                                }
                            ],
                        },
                        "finish_reason": "tool_calls",
                    }
                ],
            },
        )

    def test_multiple_tool_calls_on_same_choice(self):
        """Two tool calls on the same choice, different indexes."""
        chunks = [
            _single_choice_chunk(
                role="assistant",
                tool_calls=[
                    ToolCall(
                        id="tc-1",
                        index=0,
                        function=FunctionCall(
                            name="get_weather", arguments='{"location": "Paris"}'
                        ),
                    ),
                    ToolCall(
                        id="tc-2",
                        index=1,
                        function=FunctionCall(
                            name="get_time", arguments='{"timezone": "CET"}'
                        ),
                    ),
                ],
                finish_reason="tool_calls",
            ),
        ]
        result = accumulate_chunks_to_response_dict(chunks)

        self.assertDictEqual(
            result,
            {
                "id": _DEFAULT_ID,
                "model": _DEFAULT_MODEL,
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": "tc-1",
                                    "function": {
                                        "name": "get_weather",
                                        "arguments": '{"location": "Paris"}',
                                    },
                                },
                                {
                                    "id": "tc-2",
                                    "function": {
                                        "name": "get_time",
                                        "arguments": '{"timezone": "CET"}',
                                    },
                                },
                            ],
                        },
                        "finish_reason": "tool_calls",
                    }
                ],
            },
        )

    def test_multiple_choices(self):
        """n > 1: parallel choice accumulation."""
        chunks = [
            CompletionChunk(
                id=_DEFAULT_ID,
                model=_DEFAULT_MODEL,
                choices=[
                    CompletionResponseStreamChoice(
                        index=0,
                        delta=DeltaMessage(role="assistant", content="Answer A"),
                        finish_reason=None,
                    ),
                    CompletionResponseStreamChoice(
                        index=1,
                        delta=DeltaMessage(role="assistant", content="Answer B"),
                        finish_reason=None,
                    ),
                ],
            ),
            CompletionChunk(
                id=_DEFAULT_ID,
                model=_DEFAULT_MODEL,
                choices=[
                    CompletionResponseStreamChoice(
                        index=0, delta=DeltaMessage(content=""), finish_reason="stop"
                    ),
                    CompletionResponseStreamChoice(
                        index=1, delta=DeltaMessage(content=""), finish_reason="stop"
                    ),
                ],
            ),
        ]
        result = accumulate_chunks_to_response_dict(chunks)

        self.assertDictEqual(
            result,
            {
                "id": _DEFAULT_ID,
                "model": _DEFAULT_MODEL,
                "choices": [
                    {
                        "message": {"role": "assistant", "content": "Answer A"},
                        "finish_reason": "stop",
                    },
                    {
                        "message": {"role": "assistant", "content": "Answer B"},
                        "finish_reason": "stop",
                    },
                ],
            },
        )

    def test_missing_usage(self):
        """Interrupted stream — no usage in any chunk."""
        chunks = [
            _single_choice_chunk(role="assistant", content="partial"),
        ]
        result = accumulate_chunks_to_response_dict(chunks)

        self.assertDictEqual(
            result,
            {
                "id": _DEFAULT_ID,
                "model": _DEFAULT_MODEL,
                "choices": [
                    {
                        "message": {"role": "assistant", "content": "partial"},
                        "finish_reason": "",
                    }
                ],
            },
        )

    def test_function_name_accumulation(self):
        """Function name split across chunks."""
        chunks = [
            _single_choice_chunk(
                tool_calls=[
                    ToolCall(
                        id="tc-1",
                        index=0,
                        function=FunctionCall(name="get_", arguments=""),
                    )
                ],
            ),
            _single_choice_chunk(
                tool_calls=[
                    ToolCall(
                        index=0,
                        function=FunctionCall(
                            name="weather", arguments='{"loc": "Paris"}'
                        ),
                    )
                ],
                finish_reason="tool_calls",
            ),
        ]
        result = accumulate_chunks_to_response_dict(chunks)

        self.assertDictEqual(
            result,
            {
                "id": _DEFAULT_ID,
                "model": _DEFAULT_MODEL,
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": "tc-1",
                                    "function": {
                                        "name": "get_weather",
                                        "arguments": '{"loc": "Paris"}',
                                    },
                                }
                            ],
                        },
                        "finish_reason": "tool_calls",
                    }
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
