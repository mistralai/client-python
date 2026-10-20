import pytest

from mistralai.extra.voice_agents.tools import FunctionHandler, function_tool


def test_schema_and_description_from_signature():
    @function_tool
    def get_weather(city: str, days: int = 1, **kwargs) -> dict:
        """Return the weather for a city."""
        return {"city": city, "days": days}

    assert isinstance(get_weather, FunctionHandler)
    wire = get_weather.to_wire()["function"]
    assert wire["name"] == "get_weather"
    assert wire["description"] == "Return the weather for a city."
    props = wire["parameters"]["properties"]
    assert props["city"]["type"] == "string"
    assert props["days"]["type"] == "integer"
    assert wire["parameters"]["required"] == ["city"]  # days has a default
    assert wire["parameters"]["additionalProperties"] is True
    assert (
        get_weather.signature_mismatch({"properties": {"city": {}, "country": {}}})
        is None
    )
    mismatch = get_weather.signature_mismatch({"properties": {}})
    assert mismatch is not None and "requires city" in mismatch


def test_tool_without_docstring_omits_description():
    @function_tool
    def ping() -> str:
        return "pong"

    assert "description" not in ping.to_wire()["function"]


def test_name_override():
    @function_tool(name="getWeather")
    def get_weather(city: str) -> None: ...

    assert get_weather.name == "getWeather"


@pytest.mark.asyncio
async def test_invoke_serializes_and_validates():
    @function_tool
    def echo(message: str, **kwargs) -> dict:
        return {"echoed": message, **kwargs}

    # dict result -> JSON string
    assert await echo.invoke('{"message": "hi"}') == '{"echoed": "hi"}'
    assert (
        await echo.invoke('{"message": "hi", "city": "Paris"}')
        == '{"echoed": "hi", "city": "Paris"}'
    )

    # plain str result passes through unquoted
    @function_tool
    def shout(text: str) -> str:
        return text.upper()

    assert await shout.invoke('{"text": "hi"}') == "HI"

    # None -> empty string
    @function_tool
    def noop(x: int) -> None:
        return None

    assert await noop.invoke('{"x": 1}') == ""


@pytest.mark.asyncio
async def test_invoke_awaits_async_handler():
    @function_tool
    async def add(a: int, b: int, **kwargs) -> int:
        return a + b + kwargs.get("bonus", 0)

    assert await add.invoke('{"a": 2, "b": 3}') == "5"
    assert await add.invoke('{"a": 2, "b": 3, "bonus": 4}') == "9"


@pytest.mark.asyncio
async def test_invoke_rejects_bad_arguments():
    @function_tool
    def needs_int(n: int) -> int:
        return n

    with pytest.raises(Exception):
        await needs_int.invoke('{"n": "not-a-number"}')
