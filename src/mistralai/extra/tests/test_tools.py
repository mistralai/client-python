"""Unit tests for create_tool_call parameter description propagation.

Validates that parameter descriptions from docstrings and Annotated[T, Field(...)]
annotations correctly appear in the JSON schema produced by create_tool_call().

This is a regression test for a Pydantic v2 bug where post-construction mutation
of FieldInfo.description is silently ignored by model_json_schema().

Fixtures are defined inline so each test is self-contained.
"""

import unittest
from typing import Annotated, Optional

from pydantic import Field

from ..run.tools import create_tool_call


def _props(func):
    """Shorthand: create a tool call and return its parameter properties."""
    return create_tool_call(func).function.parameters["properties"]


class TestCreateToolCallDescriptions(unittest.TestCase):
    """Descriptions from docstrings must appear in the generated JSON schema."""

    # -- Docstring descriptions (Path 3: no existing FieldInfo) ----------------

    def test_required_param_gets_docstring_description(self):
        def search(query: str) -> str:
            """Search the web.

            Args:
                query: The search query to execute.
            """
            return ""

        props = _props(search)
        self.assertEqual(props["query"]["description"], "The search query to execute.")

    def test_optional_param_with_default_gets_docstring_description(self):
        def search(query: str, limit: int = 10) -> str:
            """Search the web.

            Args:
                query: The search query.
                limit: Maximum number of results.
            """
            return ""

        props = _props(search)
        self.assertEqual(props["limit"]["description"], "Maximum number of results.")
        self.assertEqual(props["limit"]["default"], 10)

    def test_multiple_params_all_get_descriptions(self):
        def fetch(url: str, timeout: int = 30, verbose: bool = False) -> str:
            """Fetch a URL.

            Args:
                url: The URL to fetch.
                timeout: Request timeout in seconds.
                verbose: Enable verbose logging.
            """
            return ""

        props = _props(fetch)
        self.assertEqual(props["url"]["description"], "The URL to fetch.")
        self.assertEqual(props["timeout"]["description"], "Request timeout in seconds.")
        self.assertEqual(props["verbose"]["description"], "Enable verbose logging.")

    # -- Annotated + docstring (Path 2: existing FieldInfo) --------------------

    def test_annotated_field_description_overridden_by_docstring(self):
        def search(query: Annotated[str, Field(description="original")]) -> str:
            """Search.

            Args:
                query: From docstring.
            """
            return ""

        props = _props(search)
        self.assertEqual(props["query"]["description"], "From docstring.")

    def test_annotated_field_description_preserved_when_no_docstring_entry(self):
        """When the docstring has no Args entry for a param, the Field(description=...)
        from Annotated must be preserved, not clobbered with empty string."""

        def search(query: Annotated[str, Field(description="keep me")]) -> str:
            """Search the web."""
            return ""

        props = _props(search)
        self.assertEqual(props["query"]["description"], "keep me")

    def test_annotated_field_constraints_preserved_with_docstring(self):
        def count(n: Annotated[int, Field(ge=0, le=100)]) -> str:
            """Count items.

            Args:
                n: Number of items.
            """
            return ""

        props = _props(count)
        self.assertEqual(props["n"]["description"], "Number of items.")
        self.assertEqual(props["n"]["minimum"], 0)
        self.assertEqual(props["n"]["maximum"], 100)

    def test_annotated_field_constraints_preserved_without_docstring_entry(self):
        def count(
            n: Annotated[int, Field(ge=0, le=100, description="original")],
        ) -> str:
            """Count items."""
            return ""

        props = _props(count)
        self.assertEqual(props["n"]["description"], "original")
        self.assertEqual(props["n"]["minimum"], 0)
        self.assertEqual(props["n"]["maximum"], 100)

    # -- Field as default value (Path 1: isinstance(default, FieldInfo)) -------

    def test_field_default_value_with_docstring(self):
        def search(query: str, limit: int = Field(default=10, ge=1)) -> str:
            """Search.

            Args:
                query: The query.
                limit: Max results.
            """
            return ""

        props = _props(search)
        self.assertEqual(props["limit"]["description"], "Max results.")
        self.assertEqual(props["limit"]["default"], 10)
        self.assertEqual(props["limit"]["minimum"], 1)

    def test_field_default_value_without_docstring_entry(self):
        """Field(default=..., ge=...) without a docstring entry should preserve
        constraints and not inject a spurious empty description."""

        def search(query: str, limit: int = Field(default=10, ge=1)) -> str:
            """Search.

            Args:
                query: The query.
            """
            return ""

        props = _props(search)
        self.assertEqual(props["limit"]["default"], 10)
        self.assertEqual(props["limit"]["minimum"], 1)

    # -- Edge cases ------------------------------------------------------------

    def test_undocumented_param_has_no_description_key(self):
        """Params without any docstring entry or Field description should not
        have a description key in the schema (not even an empty string)."""

        def search(query: str) -> str:
            """Search the web."""
            return ""

        props = _props(search)
        self.assertIn("query", props)
        self.assertNotIn("description", props["query"])

    def test_required_params_in_required_list(self):
        def search(query: str, limit: int = 10) -> str:
            """Search.

            Args:
                query: The query.
                limit: Max results.
            """
            return ""

        tool = create_tool_call(search)
        required = tool.function.parameters.get("required", [])
        self.assertIn("query", required)
        self.assertNotIn("limit", required)

    def test_optional_type_annotation(self):
        def search(query: str, tag: Optional[str] = None) -> str:
            """Search.

            Args:
                query: The query.
                tag: Optional tag filter.
            """
            return ""

        props = _props(search)
        self.assertEqual(props["tag"]["description"], "Optional tag filter.")

    def test_list_type_annotation(self):
        def search(queries: list[str]) -> str:
            """Batch search.

            Args:
                queries: List of search queries.
            """
            return ""

        props = _props(search)
        self.assertEqual(props["queries"]["description"], "List of search queries.")

    def test_function_level_description(self):
        def search(query: str) -> str:
            """Search the web for information.

            Args:
                query: The search query.
            """
            return ""

        tool = create_tool_call(search)
        self.assertEqual(tool.function.description, "Search the web for information.")

    def test_no_docstring_at_all(self):
        def search(query: str) -> str:
            return ""

        tool = create_tool_call(search)
        self.assertIsNotNone(tool.function.parameters)
        self.assertIn("query", tool.function.parameters["properties"])

    def test_shared_field_info_no_cross_contamination(self):
        """Two functions sharing the same FieldInfo instance via Annotated must
        not cross-contaminate descriptions."""

        shared_field = Field(ge=0)

        def func_a(n: Annotated[int, shared_field]) -> str:
            """A.

            Args:
                n: Description A.
            """
            return ""

        def func_b(n: Annotated[int, shared_field]) -> str:
            """B.

            Args:
                n: Description B.
            """
            return ""

        props_a = _props(func_a)
        props_b = _props(func_b)
        self.assertEqual(props_a["n"]["description"], "Description A.")
        self.assertEqual(props_b["n"]["description"], "Description B.")
        # Calling func_a again after func_b must still produce "Description A."
        props_a_again = _props(func_a)
        self.assertEqual(props_a_again["n"]["description"], "Description A.")
        # Original shared instance must be unmodified
        self.assertIsNone(shared_field.description)


class TestCreateToolCallRegressionPydanticV2(unittest.TestCase):
    """Regression: post-construction FieldInfo.description mutation is broken in Pydantic v2."""

    def test_description_appears_in_schema_not_silently_dropped(self):
        """The original bug: docstring descriptions were silently dropped from the
        JSON schema because FieldInfo.description was mutated after construction,
        which Pydantic v2 ignores in model_json_schema()."""

        def get_weather(city: str, units: str = "celsius") -> str:
            """Get weather for a city.

            Args:
                city: The city name.
                units: Temperature units.
            """
            return ""

        tool = create_tool_call(get_weather)
        props = tool.function.parameters["properties"]
        self.assertEqual(props["city"]["description"], "The city name.")
        self.assertEqual(props["units"]["description"], "Temperature units.")
        self.assertEqual(props["units"]["default"], "celsius")


if __name__ == "__main__":
    unittest.main()
