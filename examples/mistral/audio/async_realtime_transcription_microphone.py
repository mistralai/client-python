#!/usr/bin/env python
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "mistralai[realtime]",
#   "pyaudio",
#   "rich",
# ]
# [tool.uv.sources]
# mistralai = { path = "../../..", editable = true }
# ///

import argparse
import asyncio
import os
import sys
from typing import AsyncIterator

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from mistralai import Mistral
from mistralai.extra.realtime import UnknownRealtimeEvent
from mistralai.models import (
    AudioFormat,
    RealtimeTranscriptionError,
    RealtimeTranscriptionSessionCreated,
    TranscriptionStreamDone,
    TranscriptionStreamTextDelta,
)

console = Console()


class TranscriptDisplay:
    """Manages the live transcript display."""

    def __init__(self, model: str) -> None:
        self.model = model
        self.transcript = ""
        self.status = "🔌 Connecting..."
        self.error: str | None = None

    def set_listening(self) -> None:
        self.status = "🎤 Listening..."

    def add_text(self, text: str) -> None:
        self.transcript += text

    def set_done(self) -> None:
        self.status = "✅ Done"

    def set_error(self, error: str) -> None:
        self.status = "❌ Error"
        self.error = error

    def render(self) -> Layout:
        layout = Layout()

        # Create minimal header
        header_text = Text()
        header_text.append("│ ", style="dim")
        header_text.append(self.model, style="dim")
        header_text.append(" │ ", style="dim")

        if "Listening" in self.status:
            status_style = "green"
        elif "Connecting" in self.status:
            status_style = "yellow dim"
        elif "Done" in self.status or "Stopped" in self.status:
            status_style = "dim"
        else:
            status_style = "red"
        header_text.append(self.status, style=status_style)

        header = Align.left(header_text, vertical="middle", pad=False)

        # Create main transcript area - no title, minimal border
        transcript_text = Text(
            self.transcript or "...", style="white" if self.transcript else "dim"
        )
        transcript = Panel(
            Align.left(transcript_text, vertical="top"),
            border_style="dim",
            padding=(1, 2),
        )

        # Minimal footer
        footer_text = Text()
        footer_text.append("ctrl+c", style="dim")
        footer_text.append(" quit", style="dim italic")
        footer = Align.left(footer_text, vertical="middle", pad=False)

        # Handle error display
        if self.error:
            layout.split_column(
                Layout(header, name="header", size=1),
                Layout(transcript, name="body"),
                Layout(
                    Panel(Text(self.error, style="red"), border_style="red"),
                    name="error",
                    size=4,
                ),
                Layout(footer, name="footer", size=1),
            )
        else:
            layout.split_column(
                Layout(header, name="header", size=1),
                Layout(transcript, name="body"),
                Layout(footer, name="footer", size=1),
            )

        return layout


async def iter_microphone(
    *,
    sample_rate: int,
    chunk_duration_ms: int,
) -> AsyncIterator[bytes]:
    """
    Yield microphone PCM chunks using PyAudio (16-bit mono).
    Encoding is always pcm_s16le.
    """
    import pyaudio

    p = pyaudio.PyAudio()
    chunk_samples = int(sample_rate * chunk_duration_ms / 1000)

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_samples,
    )

    loop = asyncio.get_running_loop()
    try:
        while True:
            # stream.read is blocking; run it off-thread
            data = await loop.run_in_executor(None, stream.read, chunk_samples, False)
            yield data
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Real-time microphone transcription.")
    parser.add_argument("--model", default="voxtral-mini-transcribe-realtime-2602", help="Model ID")
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        choices=[8000, 16000, 22050, 44100, 48000],
        help="Sample rate in Hz",
    )
    parser.add_argument(
        "--chunk-duration", type=int, default=10, help="Chunk duration in ms"
    )
    parser.add_argument(
        "--api-key", default=os.environ.get("MISTRAL_API_KEY"), help="Mistral API key"
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("MISTRAL_BASE_URL", "wss://api.mistral.ai"),
    )
    return parser.parse_args()


async def main() -> int:
    args = parse_args()
    api_key = args.api_key or os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key, server_url=args.base_url)

    # microphone is always pcm_s16le here
    audio_format = AudioFormat(encoding="pcm_s16le", sample_rate=args.sample_rate)

    mic_stream = iter_microphone(
        sample_rate=args.sample_rate, chunk_duration_ms=args.chunk_duration
    )

    display = TranscriptDisplay(model=args.model)

    with Live(
        display.render(), console=console, refresh_per_second=10, screen=True
    ) as live:
        try:
            async for event in client.audio.realtime.transcribe_stream(
                audio_stream=mic_stream,
                model=args.model,
                audio_format=audio_format,
            ):
                if isinstance(event, RealtimeTranscriptionSessionCreated):
                    display.set_listening()
                    live.update(display.render())
                elif isinstance(event, TranscriptionStreamTextDelta):
                    display.add_text(event.text)
                    live.update(display.render())
                elif isinstance(event, TranscriptionStreamDone):
                    display.set_done()
                    live.update(display.render())
                    break
                elif isinstance(event, RealtimeTranscriptionError):
                    display.set_error(str(event.error))
                    live.update(display.render())
                    return 1
                elif isinstance(event, UnknownRealtimeEvent):
                    continue
        except KeyboardInterrupt:
            display.status = "⏹️ Stopped"
            live.update(display.render())

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
