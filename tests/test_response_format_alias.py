"""Test that response_format_from_pydantic_model respects Pydantic field aliases."""

from pydantic import BaseModel, Field

from mistralai.extra.utils.response_format import response_format_from_pydantic_model


class AliasedModel(BaseModel):
    full_name: str = Field(alias="fullName")
    phone_number: str = Field(alias="phoneNumber")


class NoAliasModel(BaseModel):
    name: str
    age: int


def test_response_format_uses_alias_keys():
    """Schema properties should use alias names, not Python field names."""
    result = response_format_from_pydantic_model(AliasedModel)
    schema = result.json_schema.schema_definition

    props = schema["properties"]
    assert "fullName" in props, f"Expected 'fullName' in properties, got {list(props)}"
    assert "phoneNumber" in props, f"Expected 'phoneNumber' in properties, got {list(props)}"
    assert "full_name" not in props, "Python field name 'full_name' should not appear"
    assert "phone_number" not in props, "Python field name 'phone_number' should not appear"


def test_response_format_required_uses_aliases():
    """Required field list should use alias names."""
    result = response_format_from_pydantic_model(AliasedModel)
    schema = result.json_schema.schema_definition

    required = schema["required"]
    assert "fullName" in required
    assert "phoneNumber" in required


def test_response_format_without_aliases_unchanged():
    """Models without aliases should work as before."""
    result = response_format_from_pydantic_model(NoAliasModel)
    schema = result.json_schema.schema_definition

    props = schema["properties"]
    assert "name" in props
    assert "age" in props
