#!/usr/bin/env python

import os

from mistralai.client import Mistral


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    print("Using the .complete method to input a raw json schema to the API:\n")
    # When providing raw JSON Schema to the SDK you need to have 'additionalProperties': False in the schema definition
    # This is because the API is only accepting a strict JSON Schema
    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful math tutor. You will be provided with a math problem, and your goal will be to output a step by step solution, along with a final answer. For each step, just provide the output as an equation use the explanation field to detail the reasoning.",
            },
            {"role": "user", "content": "How can I solve 8x + 7 = -23"},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "MathDemonstration",
                "schema_definition": {
                    "$defs": {
                        "Explanation": {
                            "properties": {
                                "explanation": {
                                    "title": "Explanation",
                                    "type": "string",
                                },
                                "output": {"title": "Output", "type": "string"},
                            },
                            "required": ["explanation", "output"],
                            "title": "Explanation",
                            "type": "object",
                            "additionalProperties": False,
                        }
                    },
                    "properties": {
                        "steps": {
                            "items": {"$ref": "#/$defs/Explanation"},
                            "title": "Steps",
                            "type": "array",
                        },
                        "final_answer": {"title": "Final Answer", "type": "string"},
                    },
                    "required": ["steps", "final_answer"],
                    "title": "MathDemonstration",
                    "type": "object",
                    "additionalProperties": False,
                },
                "description": None,
                "strict": True,
            },
        },
    )
    print(chat_response.choices[0].message.content)

    # Or with the streaming API
    with client.chat.stream(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful math tutor. You will be provided with a math problem, and your goal will be to output a step by step solution, along with a final answer. For each step, just provide the output as an equation use the explanation field to detail the reasoning.",
            },
            {"role": "user", "content": "How can I solve 8x + 7 = -23"},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "MathDemonstration",
                "schema_definition": {
                    "$defs": {
                        "Explanation": {
                            "properties": {
                                "explanation": {
                                    "title": "Explanation",
                                    "type": "string",
                                },
                                "output": {"title": "Output", "type": "string"},
                            },
                            "required": ["explanation", "output"],
                            "title": "Explanation",
                            "type": "object",
                            "additionalProperties": False,
                        }
                    },
                    "properties": {
                        "steps": {
                            "items": {"$ref": "#/$defs/Explanation"},
                            "title": "Steps",
                            "type": "array",
                        },
                        "final_answer": {"title": "Final Answer", "type": "string"},
                    },
                    "required": ["steps", "final_answer"],
                    "title": "MathDemonstration",
                    "type": "object",
                    "additionalProperties": False,
                },
                "description": None,
                "strict": True,
            },
        },
    ) as stream:
        for chunk in stream:
            print(chunk.data.choices[0].delta.content, end="")


if __name__ == "__main__":
    main()
