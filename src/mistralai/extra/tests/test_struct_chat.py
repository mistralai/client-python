import unittest
from ..struct_chat import (
    convert_to_parsed_chat_completion_response,
    ParsedChatCompletionResponse,
    ParsedChatCompletionChoice,
    ParsedAssistantMessage,
)
from ...models import (
    ChatCompletionResponse,
    UsageInfo,
    ChatCompletionChoice,
    AssistantMessage,
)
from pydantic import BaseModel


class Explanation(BaseModel):
    explanation: str
    output: str


class MathDemonstration(BaseModel):
    steps: list[Explanation]
    final_answer: str


mock_cc_response = ChatCompletionResponse(
    id="c0271b2098954c6094231703875ca0bc",
    object="chat.completion",
    model="mistral-large-latest",
    usage=UsageInfo(prompt_tokens=75, completion_tokens=220, total_tokens=295),
    created=1737727558,
    choices=[
        ChatCompletionChoice(
            index=0,
            message=AssistantMessage(
                content='{\n  "final_answer": "x = -4",\n  "steps": [\n    {\n      "explanation": "Start with the given equation.",\n      "output": "8x + 7 = -23"\n    },\n    {\n      "explanation": "Subtract 7 from both sides to isolate the term with x.",\n      "output": "8x = -23 - 7"\n    },\n    {\n      "explanation": "Simplify the right side of the equation.",\n      "output": "8x = -30"\n    },\n    {\n      "explanation": "Divide both sides by 8 to solve for x.",\n      "output": "x = -30 / 8"\n    },\n    {\n      "explanation": "Simplify the fraction to get the final answer.",\n      "output": "x = -4"\n    }\n  ]\n}',
                tool_calls=None,
                prefix=False,
                role="assistant",
            ),
            finish_reason="stop",
        )
    ],
)


expected_response: ParsedChatCompletionResponse = ParsedChatCompletionResponse(
    choices=[
        ParsedChatCompletionChoice(
            index=0,
            message=ParsedAssistantMessage(
                content='{\n  "final_answer": "x = -4",\n  "steps": [\n    {\n      "explanation": "Start with the given equation.",\n      "output": "8x + 7 = -23"\n    },\n    {\n      "explanation": "Subtract 7 from both sides to isolate the term with x.",\n      "output": "8x = -23 - 7"\n    },\n    {\n      "explanation": "Simplify the right side of the equation.",\n      "output": "8x = -30"\n    },\n    {\n      "explanation": "Divide both sides by 8 to solve for x.",\n      "output": "x = -30 / 8"\n    },\n    {\n      "explanation": "Simplify the fraction to get the final answer.",\n      "output": "x = -4"\n    }\n  ]\n}',
                tool_calls=None,
                prefix=False,
                role="assistant",
                parsed=MathDemonstration(
                    steps=[
                        Explanation(
                            explanation="Start with the given equation.",
                            output="8x + 7 = -23",
                        ),
                        Explanation(
                            explanation="Subtract 7 from both sides to isolate the term with x.",
                            output="8x = -23 - 7",
                        ),
                        Explanation(
                            explanation="Simplify the right side of the equation.",
                            output="8x = -30",
                        ),
                        Explanation(
                            explanation="Divide both sides by 8 to solve for x.",
                            output="x = -30 / 8",
                        ),
                        Explanation(
                            explanation="Simplify the fraction to get the final answer.",
                            output="x = -4",
                        ),
                    ],
                    final_answer="x = -4",
                ),
            ),
            finish_reason="stop",
        )
    ],
    created=1737727558,
    id="c0271b2098954c6094231703875ca0bc",
    model="mistral-large-latest",
    object="chat.completion",
    usage=UsageInfo(prompt_tokens=75, completion_tokens=220, total_tokens=295),
)


class TestConvertToParsedChatCompletionResponse(unittest.TestCase):
    def test_convert_to_parsed_chat_completion_response(self):
        output = convert_to_parsed_chat_completion_response(
            mock_cc_response, MathDemonstration
        )
        self.assertEqual(output, expected_response)

    def test_empty_string_content(self):
        """Test that empty string content is handled gracefully (issue #282)"""
        response = ChatCompletionResponse(
            id="test-empty",
            object="chat.completion",
            model="codestral-latest",
            usage=UsageInfo(prompt_tokens=10, completion_tokens=0, total_tokens=10),
            created=1234567890,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content="",  # Empty string
                        tool_calls=None,
                        prefix=False,
                        role="assistant",
                    ),
                    finish_reason="stop",
                )
            ],
        )

        # Should not raise JSONDecodeError
        result = convert_to_parsed_chat_completion_response(response, MathDemonstration)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.choices), 1)
        self.assertIsNone(result.choices[0].message.parsed)

    def test_whitespace_only_content(self):
        """Test that whitespace-only content is handled gracefully (issue #282)"""
        response = ChatCompletionResponse(
            id="test-whitespace",
            object="chat.completion",
            model="codestral-latest",
            usage=UsageInfo(prompt_tokens=10, completion_tokens=0, total_tokens=10),
            created=1234567890,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content="   ",  # Whitespace only
                        tool_calls=None,
                        prefix=False,
                        role="assistant",
                    ),
                    finish_reason="stop",
                )
            ],
        )

        # Should not raise JSONDecodeError
        result = convert_to_parsed_chat_completion_response(response, MathDemonstration)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.choices), 1)
        self.assertIsNone(result.choices[0].message.parsed)

    def test_invalid_json_content(self):
        """Test that invalid JSON content is handled gracefully (issue #282)"""
        response = ChatCompletionResponse(
            id="test-invalid-json",
            object="chat.completion",
            model="codestral-latest",
            usage=UsageInfo(prompt_tokens=10, completion_tokens=20, total_tokens=30),
            created=1234567890,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content="This is not JSON at all",  # Invalid JSON
                        tool_calls=None,
                        prefix=False,
                        role="assistant",
                    ),
                    finish_reason="stop",
                )
            ],
        )

        # Should not raise JSONDecodeError
        result = convert_to_parsed_chat_completion_response(response, MathDemonstration)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.choices), 1)
        self.assertIsNone(result.choices[0].message.parsed)

    def test_none_content(self):
        """Test that None content is handled correctly"""
        response = ChatCompletionResponse(
            id="test-none",
            object="chat.completion",
            model="codestral-latest",
            usage=UsageInfo(prompt_tokens=10, completion_tokens=0, total_tokens=10),
            created=1234567890,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content=None,  # None
                        tool_calls=None,
                        prefix=False,
                        role="assistant",
                    ),
                    finish_reason="stop",
                )
            ],
        )

        result = convert_to_parsed_chat_completion_response(response, MathDemonstration)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.choices), 1)
        self.assertIsNone(result.choices[0].message.parsed)


if __name__ == "__main__":
    unittest.main()
