from ..utils.response_format import (
    pydantic_model_from_json,
    response_format_from_pydantic_model,
    rec_strict_json_schema,
)
from pydantic import BaseModel, Field, ValidationError

from ...models import ResponseFormat, JSONSchema
from ...types.basemodel import Unset

import unittest


class Student(BaseModel):
    name: str
    age: int


class Explanation(BaseModel):
    explanation: str
    output: str


class MathDemonstration(BaseModel):
    steps: list[Explanation]
    final_answer: str


mathdemo_schema = {
    "$defs": {
        "Explanation": {
            "properties": {
                "explanation": {"title": "Explanation", "type": "string"},
                "output": {"title": "Output", "type": "string"},
            },
            "required": ["explanation", "output"],
            "title": "Explanation",
            "type": "object",
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
}

mathdemo_strict_schema = mathdemo_schema.copy()
mathdemo_strict_schema["$defs"]["Explanation"]["additionalProperties"] = False # type: ignore
mathdemo_strict_schema["additionalProperties"] = False

mathdemo_response_format = ResponseFormat(
    type="json_schema",
    json_schema=JSONSchema(
        name="MathDemonstration",
        schema_definition=mathdemo_strict_schema,
        description=Unset(),
        strict=True,
    ),
)


class TestResponseFormat(unittest.TestCase):
    def test_pydantic_model_from_json(self):
        missing_json_data = {"name": "Jean Dupont"}
        good_json_data = {"name": "Jean Dupont", "age": 25}
        extra_json_data = {
            "name": "Jean Dupont",
            "age": 25,
            "extra_field": "extra_value",
        }
        complex_json_data = {
            "final_answer": "x = -4",
            "steps": [
                {
                    "explanation": "Start with the given equation.",
                    "output": "8x + 7 = -23",
                },
                {
                    "explanation": "Subtract 7 from both sides to isolate the term with x.",
                    "output": "8x = -23 - 7",
                },
                {
                    "explanation": "Simplify the right side of the equation.",
                    "output": "8x = -30",
                },
                {
                    "explanation": "Divide both sides by 8 to solve for x.",
                    "output": "x = -30 / 8",
                },
                {
                    "explanation": "Simplify the fraction to get the final answer.",
                    "output": "x = -4",
                },
            ],
        }

        self.assertEqual(
            pydantic_model_from_json(good_json_data, Student),
            Student(name="Jean Dupont", age=25),
        )
        self.assertEqual(
            pydantic_model_from_json(extra_json_data, Student),
            Student(name="Jean Dupont", age=25),
        )
        self.assertEqual(
            pydantic_model_from_json(complex_json_data, MathDemonstration),
            MathDemonstration(
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
        )

        # Check it raises a validation error
        with self.assertRaises(ValidationError):
            pydantic_model_from_json(missing_json_data, Student)  # type: ignore

    def test_response_format_from_pydantic_model(self):
        self.assertEqual(
            response_format_from_pydantic_model(MathDemonstration),
            mathdemo_response_format,
        )

    def test_rec_strict_json_schema(self):
        self.assertEqual(
            rec_strict_json_schema(mathdemo_schema), mathdemo_strict_schema
        )

    def test_rec_strict_json_schema_with_numeric_constraints(self):
        """
        Test that rec_strict_json_schema handles JSON Schema constraint keywords
        that have numeric values (e.g., minLength, maxLength, minItems, maxItems).

        This is a regression test for issue #300 where Pydantic models with
        constraint keywords like min_length would cause a ValueError.
        """
        # Schema with numeric constraint values (minItems, maxItems, minimum, etc.)
        schema_with_constraints = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "minItems": 1,
                    "maxItems": 10,
                },
                "name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 100,
                },
                "count": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000,
                    "multipleOf": 0.5,  # float value
                },
            },
            "required": ["items", "name"],
        }

        # Should not raise ValueError - integers and floats are valid terminal values
        result = rec_strict_json_schema(schema_with_constraints)

        # Check that additionalProperties was added
        self.assertEqual(result["additionalProperties"], False)
        # Check that numeric constraints are preserved
        self.assertEqual(result["properties"]["items"]["minItems"], 1)
        self.assertEqual(result["properties"]["items"]["maxItems"], 10)
        self.assertEqual(result["properties"]["name"]["minLength"], 1)
        self.assertEqual(result["properties"]["count"]["multipleOf"], 0.5)

    def test_response_format_with_constrained_pydantic_model(self):
        """
        Test that response_format_from_pydantic_model works with Pydantic models
        that use constraint keywords like min_length.

        This is a regression test for issue #300.
        """

        class ModelWithConstraints(BaseModel):
            some_list: list[int] = Field(
                default_factory=list,
                description="A list of integers",
                min_length=1,
            )
            name: str = Field(
                description="A name",
                min_length=1,
                max_length=100,
            )

        # Should not raise ValueError
        result = response_format_from_pydantic_model(ModelWithConstraints)

        # Verify it returns a valid ResponseFormat
        self.assertIsInstance(result, ResponseFormat)
        self.assertEqual(result.type, "json_schema")
        self.assertIsNotNone(result.json_schema)

    def test_rec_strict_json_schema_with_invalid_type(self):
        """Test that rec_strict_json_schema raises ValueError for truly invalid types."""
        # A custom object that is not a valid JSON schema node type
        class CustomObject:
            pass

        invalid_schema = {"invalid": CustomObject()}

        with self.assertRaises(ValueError):
            rec_strict_json_schema(invalid_schema)


if __name__ == "__main__":
    unittest.main()
