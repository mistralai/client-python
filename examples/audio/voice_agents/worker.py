"""Example: run a custom LiveKit worker with only a Mistral API key.

    pip install "mistralai[voice-agents]" "livekit-agents[mistralai]"
    export MISTRAL_API_KEY=...            # your workspace key
    export MISTRAL_AUDIO_BASE_URL=...     # the audio control-plane URL
    python examples/audio/voice_agents/worker.py dev

The control plane exchanges your Mistral key for a short-lived registration
token; you never handle a LiveKit URL, key, or secret. You own everything inside
``entrypoint`` — any pipeline, any third-party model.
"""

from livekit.agents import Agent, AgentSession, JobContext
from livekit.plugins import mistralai

from mistralai.extra.voice_agents.worker import run_worker


async def entrypoint(ctx: JobContext) -> None:
    await ctx.connect()
    session = AgentSession(
        stt=mistralai.STT(),
        llm=mistralai.LLM(),
        tts=mistralai.TTS(),
    )
    await session.start(
        agent=Agent(instructions="You are a helpful voice assistant."),
        room=ctx.room,
    )


if __name__ == "__main__":
    run_worker(entrypoint)
