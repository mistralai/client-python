"""Run with mistralai[voice-agents] and a configured MISTRAL_API_KEY."""
import asyncio

from mistralai.client import Mistral
from mistralai.extra.voice_agents import DefaultAudioInterface, WebSearchTool, function_tool


@function_tool(filler={"text": "Let me check the weather."}, timeout_ms=15000)
async def get_weather(city: str) -> dict[str, object]:
    """Return demonstration weather data for a city."""
    return {"city": city, "temp_c": 21, "conditions": "sunny"}


async def main() -> None:
    async with Mistral() as client:
        session = await client.audio.sessions.init(
            stt={"model": "voxtral-mini-transcribe-realtime-3"},
            tts={"model": "voxtral-mini-tts-3"},
            instructions="Be concise. Use get_weather for weather and web_search for current information.",
            welcome_message="Hey. Ask me about the weather somewhere.",
            tools=[WebSearchTool(), get_weather],
            audio_interface=DefaultAudioInterface(),
        )
        session.on("connected", lambda event: print("Connected:", event.session_id))
        session.on("transcript", lambda event: print(event.role, event.content))
        session.on("tool_call_started", lambda event: print("Tool started:", event.name))
        session.on("tool_call_ended", lambda event: print("Tool ended:", event.name, event.result))
        session.on("agent_state_changed", lambda event: print("State:", event.state))
        session.on("error", lambda event: print("Error:", event.model_dump_json()))
        async with session:
            await session.wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
