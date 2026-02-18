"""Test for JSONSchema serialization with and without by_alias parameter."""
import json
from mistralai.extra.utils.response_format import response_format_from_pydantic_model
from pydantic import BaseModel, Field


class TestModel(BaseModel):
    name: str = Field(description="A name field")
    value: int = Field(description="A value field")


def test_jsonschema_serialization_without_by_alias():
    """Test that model_dump() works without by_alias=True."""
    response_format = response_format_from_pydantic_model(TestModel)

    # This should work without by_alias=True
    serialized = response_format.model_dump(mode='json')

    # Verify that schema is not None
    assert serialized['json_schema']['schema'] is not None, "Schema should not be None"

    # Verify that schema contains expected fields
    schema = serialized['json_schema']['schema']
    assert 'type' in schema
    assert 'properties' in schema
    assert 'name' in schema['properties']
    assert 'value' in schema['properties']


def test_jsonschema_serialization_with_by_alias():
    """Test that model_dump(by_alias=True) continues to work."""
    response_format = response_format_from_pydantic_model(TestModel)

    # This should work with by_alias=True
    serialized = response_format.model_dump(mode='json', by_alias=True)

    # Verify that schema is not None
    assert serialized['json_schema']['schema'] is not None, "Schema should not be None"

    # Verify that schema contains expected fields
    schema = serialized['json_schema']['schema']
    assert 'type' in schema
    assert 'properties' in schema
    assert 'name' in schema['properties']
    assert 'value' in schema['properties']


def test_jsonschema_serialization_consistency():
    """Test that both serialization methods produce the same result."""
    response_format = response_format_from_pydantic_model(TestModel)

    serialized_without_alias = response_format.model_dump(mode='json')
    serialized_with_alias = response_format.model_dump(mode='json', by_alias=True)

    # Both should produce the same schema
    assert serialized_without_alias['json_schema']['schema'] == serialized_with_alias['json_schema']['schema']
