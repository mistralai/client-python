from typing import Any, TypeVar, cast

from pydantic import BaseModel, ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError
from mistralai.client.models import ResponseFormatTypedDict
from ._pydantic_helper import rec_strict_json_schema

CustomPydanticModel = TypeVar("CustomPydanticModel", bound=BaseModel)


def response_format_from_pydantic_model(
    model: type[CustomPydanticModel],
) -> ResponseFormatTypedDict:
    """Generate a strict JSON schema response format from a pydantic model.

    Returns a TypedDict compatible with both the main SDK's and Azure SDK's
    ResponseFormat / ResponseFormatTypedDict.
    """
    model_schema = rec_strict_json_schema(model.model_json_schema())
    return cast(
        ResponseFormatTypedDict,
        {
            "type": "json_schema",
            "json_schema": {
                "name": model.__name__,
                "schema": model_schema,
                "strict": True,
            },
        },
    )


def _json_type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    return type(value).__name__


def pydantic_model_from_json(
    json_data: Any,
    pydantic_model: type[CustomPydanticModel],
) -> CustomPydanticModel:
    """Parse decoded JSON into a pydantic model.

    Raises a ``ValidationError`` naming the model and the JSON type received when
    the decoded JSON is not an object (e.g. the model answered an array).
    """
    if not isinstance(json_data, dict):
        raise ValidationError.from_exception_data(
            pydantic_model.__name__,
            [
                InitErrorDetails(
                    type=PydanticCustomError(
                        "json_not_object",
                        "Expected a JSON object to parse into {model}, got a JSON {json_type}",
                        {
                            "model": pydantic_model.__name__,
                            "json_type": _json_type_name(json_data),
                        },
                    ),
                    input=json_data,
                )
            ],
        )
    return pydantic_model.model_validate(json_data)
