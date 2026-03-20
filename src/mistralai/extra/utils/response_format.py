from typing import Any, TypeVar, cast

from pydantic import BaseModel
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


def pydantic_model_from_json(
    json_data: dict[str, Any],
    pydantic_model: type[CustomPydanticModel],
) -> CustomPydanticModel:
    """Parse a JSON schema into a pydantic model."""
    return pydantic_model.model_validate(json_data)
