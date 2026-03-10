"""Unit tests for the OTEL serialization helpers.

Each test covers a single function with both happy-path and edge-case inputs.
The functions are pure (dict → str/list), so no OTEL setup is needed.
"""

import json
import unittest

from mistralai.extra.observability.serialization import (
    _content_to_parts,
    _tool_calls_to_parts,
    serialize_input_message,
    serialize_output_message,
    serialize_tool_definition,
)


def _parse(json_str: str):
    """Shorthand: parse a JSON string returned by a serialize_* function."""
    return json.loads(json_str)


class TestContentToParts(unittest.TestCase):
    def test_none(self):
        self.assertEqual(_content_to_parts(None), [])

    def test_string(self):
        self.assertEqual(
            _content_to_parts("hello"),
            [{"type": "text", "content": "hello"}],
        )

    def test_empty_string(self):
        self.assertEqual(
            _content_to_parts(""),
            [{"type": "text", "content": ""}],
        )

    def test_empty_list(self):
        self.assertEqual(_content_to_parts([]), [])

    def test_list_of_strings(self):
        self.assertEqual(
            _content_to_parts(["a", "b"]),
            [
                {"type": "text", "content": "a"},
                {"type": "text", "content": "b"},
            ],
        )

    def test_text_chunk(self):
        self.assertEqual(
            _content_to_parts([{"type": "text", "text": "hello"}]),
            [{"type": "text", "content": "hello"}],
        )

    def test_text_chunk_missing_text_field(self):
        self.assertEqual(
            _content_to_parts([{"type": "text"}]),
            [{"type": "text", "content": ""}],
        )

    # -- thinking chunks -------------------------------------------------------

    def test_thinking_chunk_with_sub_chunks(self):
        chunk = {
            "type": "thinking",
            "thinking": [
                {"type": "text", "text": "step 1"},
                {"type": "text", "text": "step 2"},
            ],
        }
        self.assertEqual(
            _content_to_parts([chunk]),
            [{"type": "reasoning", "content": "step 1\nstep 2"}],
        )

    def test_thinking_chunk_filters_non_text_sub_chunks(self):
        chunk = {
            "type": "thinking",
            "thinking": [
                {"type": "text", "text": "kept"},
                {"type": "other", "text": "ignored"},
                "also ignored",
            ],
        }
        self.assertEqual(
            _content_to_parts([chunk]),
            [{"type": "reasoning", "content": "kept"}],
        )

    def test_thinking_chunk_fallback_plain_string(self):
        chunk = {"type": "thinking", "thinking": "raw thought"}
        self.assertEqual(
            _content_to_parts([chunk]),
            [{"type": "reasoning", "content": "raw thought"}],
        )

    def test_thinking_chunk_missing_thinking_field(self):
        """Empty string default → str("") fallback."""
        chunk = {"type": "thinking"}
        self.assertEqual(
            _content_to_parts([chunk]),
            [{"type": "reasoning", "content": ""}],
        )

    # -- image_url chunks ------------------------------------------------------

    def test_image_url_chunk_dict(self):
        chunk = {"type": "image_url", "image_url": {"url": "https://img.png"}}
        self.assertEqual(
            _content_to_parts([chunk]),
            [{"type": "uri", "modality": "image", "uri": "https://img.png"}],
        )

    def test_image_url_chunk_string_fallback(self):
        chunk = {"type": "image_url", "image_url": "https://img.png"}
        self.assertEqual(
            _content_to_parts([chunk]),
            [{"type": "uri", "modality": "image", "uri": "https://img.png"}],
        )

    def test_image_url_chunk_missing_url(self):
        chunk = {"type": "image_url", "image_url": {}}
        self.assertEqual(
            _content_to_parts([chunk]),
            [{"type": "uri", "modality": "image", "uri": ""}],
        )

    # -- unknown / catch-all ---------------------------------------------------

    def test_unknown_chunk_type(self):
        chunk = {"type": "audio", "data": "..."}
        self.assertEqual(
            _content_to_parts([chunk]),
            [{"type": "audio"}],
        )

    def test_mixed_chunk_types(self):
        """Multiple chunk types in one content array."""
        parts = _content_to_parts(
            [
                {"type": "text", "text": "look at this"},
                {"type": "image_url", "image_url": {"url": "https://img.png"}},
                "plain string",
            ]
        )
        self.assertListEqual(
            parts,
            [
                {"type": "text", "content": "look at this"},
                {"type": "uri", "modality": "image", "uri": "https://img.png"},
                {"type": "text", "content": "plain string"},
            ],
        )


class TestToolCallsToParts(unittest.TestCase):
    def test_none(self):
        self.assertEqual(_tool_calls_to_parts(None), [])

    def test_empty_list(self):
        self.assertEqual(_tool_calls_to_parts([]), [])

    def test_full_tool_call(self):
        tc = {
            "id": "call_123",
            "function": {"name": "get_weather", "arguments": '{"city": "Paris"}'},
        }
        self.assertEqual(
            _tool_calls_to_parts([tc]),
            [
                {
                    "type": "tool_call",
                    "name": "get_weather",
                    "id": "call_123",
                    "arguments": '{"city": "Paris"}',
                },
            ],
        )

    def test_missing_id(self):
        tc = {"function": {"name": "f"}}
        self.assertListEqual(
            _tool_calls_to_parts([tc]),
            [{"type": "tool_call", "name": "f"}],
        )

    def test_missing_arguments(self):
        tc = {"id": "1", "function": {"name": "f"}}
        self.assertListEqual(
            _tool_calls_to_parts([tc]),
            [{"type": "tool_call", "name": "f", "id": "1"}],
        )

    def test_missing_function(self):
        """No function key → empty name."""
        tc = {"id": "1"}
        self.assertListEqual(
            _tool_calls_to_parts([tc]),
            [{"type": "tool_call", "name": "", "id": "1"}],
        )

    def test_function_is_none(self):
        tc = {"id": "1", "function": None}
        self.assertListEqual(
            _tool_calls_to_parts([tc]),
            [{"type": "tool_call", "name": "", "id": "1"}],
        )


class TestSerializeInputMessage(unittest.TestCase):
    # -- Happy paths (role-based messages) ------------------------------------

    def test_user_message(self):
        result = _parse(serialize_input_message({"role": "user", "content": "hi"}))
        self.assertDictEqual(
            result,
            {
                "role": "user",
                "parts": [{"type": "text", "content": "hi"}],
            },
        )

    def test_system_message(self):
        result = _parse(
            serialize_input_message({"role": "system", "content": "be helpful"})
        )
        self.assertDictEqual(
            result,
            {
                "role": "system",
                "parts": [{"type": "text", "content": "be helpful"}],
            },
        )

    def test_assistant_message_with_tool_calls(self):
        msg = {
            "role": "assistant",
            "content": "",
            "tool_calls": [{"id": "tc1", "function": {"name": "f", "arguments": "{}"}}],
        }
        result = _parse(serialize_input_message(msg))
        self.assertEqual(result["role"], "assistant")
        # text part from content + tool_call part
        self.assertListEqual(
            [p["type"] for p in result["parts"]],
            ["text", "tool_call"],
        )

    def test_tool_message(self):
        msg = {"role": "tool", "content": "22C sunny", "tool_call_id": "tc1"}
        result = _parse(serialize_input_message(msg))
        self.assertDictEqual(
            result,
            {
                "role": "tool",
                "parts": [
                    {"type": "tool_call_response", "response": "22C sunny", "id": "tc1"}
                ],
            },
        )

    def test_tool_message_without_tool_call_id(self):
        msg = {"role": "tool", "content": "result"}
        result = _parse(serialize_input_message(msg))
        self.assertNotIn("id", result["parts"][0])

    # -- Conversation entry: function.result ----------------------------------

    def test_function_result_entry(self):
        msg = {
            "type": "function.result",
            "result": '{"status": "ok"}',
            "tool_call_id": "tc1",
        }
        result = _parse(serialize_input_message(msg))
        self.assertDictEqual(
            result,
            {
                "role": "tool",
                "parts": [
                    {
                        "type": "tool_call_response",
                        "response": '{"status": "ok"}',
                        "id": "tc1",
                    }
                ],
            },
        )

    def test_function_result_entry_without_tool_call_id(self):
        msg = {"type": "function.result", "result": "data"}
        result = _parse(serialize_input_message(msg))
        self.assertNotIn("id", result["parts"][0])

    # -- Edge cases -----------------------------------------------------------

    def test_missing_role_defaults_to_unknown(self):
        result = _parse(serialize_input_message({"content": "orphan"}))
        self.assertDictEqual(
            result,
            {
                "role": "unknown",
                "parts": [{"type": "text", "content": "orphan"}],
            },
        )

    def test_no_content_no_tool_calls(self):
        result = _parse(serialize_input_message({"role": "user"}))
        self.assertDictEqual(result, {"role": "user", "parts": []})


class TestSerializeOutputMessage(unittest.TestCase):
    def test_simple_assistant_response(self):
        choice = {
            "message": {"role": "assistant", "content": "hello"},
            "finish_reason": "stop",
        }
        result = _parse(serialize_output_message(choice))
        self.assertDictEqual(
            result,
            {
                "role": "assistant",
                "parts": [{"type": "text", "content": "hello"}],
                "finish_reason": "stop",
            },
        )

    def test_tool_calls_response(self):
        choice = {
            "message": {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {"id": "tc1", "function": {"name": "f", "arguments": "{}"}},
                ],
            },
            "finish_reason": "tool_calls",
        }
        result = _parse(serialize_output_message(choice))
        self.assertEqual(result["finish_reason"], "tool_calls")
        self.assertListEqual(
            [p["type"] for p in result["parts"]],
            ["tool_call"],
        )

    def test_missing_message(self):
        result = _parse(serialize_output_message({}))
        self.assertDictEqual(
            result,
            {
                "role": "assistant",
                "parts": [],
                "finish_reason": "",
            },
        )

    def test_message_is_none(self):
        result = _parse(serialize_output_message({"message": None}))
        self.assertDictEqual(
            result,
            {
                "role": "assistant",
                "parts": [],
                "finish_reason": "",
            },
        )

    def test_defaults_role_to_assistant(self):
        choice = {"message": {"content": "hi"}, "finish_reason": "stop"}
        result = _parse(serialize_output_message(choice))
        self.assertDictEqual(
            result,
            {
                "role": "assistant",
                "parts": [{"type": "text", "content": "hi"}],
                "finish_reason": "stop",
            },
        )


class TestSerializeToolDefinition(unittest.TestCase):
    def test_full_definition(self):
        tool = {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather",
                "parameters": {"type": "object", "properties": {}},
            },
        }
        serialized = serialize_tool_definition(tool)
        self.assertIsNotNone(serialized)
        assert serialized is not None
        self.assertDictEqual(
            _parse(serialized),
            {
                "type": "function",
                "name": "get_weather",
                "description": "Get weather",
                "parameters": {"type": "object", "properties": {}},
            },
        )

    def test_minimal_definition(self):
        """Only name, no description or parameters."""
        tool = {"function": {"name": "f"}}
        serialized = serialize_tool_definition(tool)
        self.assertIsNotNone(serialized)
        assert serialized is not None
        self.assertDictEqual(
            _parse(serialized),
            {
                "type": "function",
                "name": "f",
            },
        )

    def test_missing_function_returns_none(self):
        self.assertIsNone(serialize_tool_definition({"type": "function"}))

    def test_empty_function_returns_none(self):
        self.assertIsNone(serialize_tool_definition({"function": {}}))

    def test_missing_name_returns_none(self):
        self.assertIsNone(
            serialize_tool_definition({"function": {"description": "no name"}})
        )

    def test_custom_type_preserved(self):
        tool = {"type": "custom_tool", "function": {"name": "f"}}
        serialized = serialize_tool_definition(tool)
        self.assertIsNotNone(serialized)
        assert serialized is not None
        self.assertDictEqual(
            _parse(serialized),
            {
                "type": "custom_tool",
                "name": "f",
            },
        )


if __name__ == "__main__":
    unittest.main()
