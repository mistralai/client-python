#!/usr/bin/env python

import argparse
import asyncio
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import AsyncIterator

from mistralai.client import Mistral
from mistralai.extra.realtime.connection import UnknownRealtimeEvent
from mistralai.client.models import (
    AudioFormat,
    RealtimeTranscriptionError,
    TranscriptionStreamDone,
    TranscriptionStreamTextDelta,
)


def convert_audio_to_pcm(
    input_path: Path,
) -> Path:
    temp_file = tempfile.NamedTemporaryFile(suffix=".pcm", delete=False)
    temp_path = Path(temp_file.name)
    temp_file.close()

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-f",
        "s16le",
        "-ar",
        str(16000),
        "-ac",
        "1",
        str(temp_path),
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg conversion failed: {exc.stderr}") from exc

    return temp_path


async def aiter_audio_file(
    path: Path,
    *,
    chunk_size: int = 4096,
    chunk_delay: float = 0.0,
) -> AsyncIterator[bytes]:
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk
            if chunk_delay > 0:
                await asyncio.sleep(chunk_delay)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Real-time audio transcription via WebSocket (iterator-based)."
    )
    parser.add_argument("file", type=Path, help="Path to the audio file")
    parser.add_argument("--model", default="voxtral-mini-2601", help="Model ID")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("MISTRAL_API_KEY"),
        help="Mistral API key",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("MISTRAL_BASE_URL", "https://api.mistral.ai"),
        help="API base URL (http/https/ws/wss)",
    )
    parser.add_argument(
        "--chunk-size", type=int, default=4096, help="Audio chunk size in bytes"
    )
    parser.add_argument(
        "--chunk-delay",
        type=float,
        default=0.01,
        help="Delay between chunks in seconds",
    )
    parser.add_argument(
        "--no-convert",
        action="store_true",
        help="Skip ffmpeg conversion (input must be raw PCM)",
    )
    return parser.parse_args()


async def main() -> int:
    args = parse_args()
    api_key = args.api_key or os.environ["MISTRAL_API_KEY"]

    pcm_path = args.file
    temp_path = None

    if not args.no_convert and args.file.suffix.lower() not in (".pcm", ".raw"):
        pcm_path = convert_audio_to_pcm(args.file)
        temp_path = pcm_path

    client = Mistral(api_key=api_key, server_url=args.base_url)

    try:
        async for event in client.audio.realtime.transcribe_stream(
            audio_stream=aiter_audio_file(
                pcm_path,
                chunk_size=args.chunk_size,
                chunk_delay=args.chunk_delay,
            ),
            model=args.model,
            audio_format=AudioFormat(encoding="pcm_s16le", sample_rate=16000),
        ):
            if isinstance(event, TranscriptionStreamTextDelta):
                print(event.text, end="", flush=True)
            elif isinstance(event, TranscriptionStreamDone):
                print()
                break
            elif isinstance(event, RealtimeTranscriptionError):
                print(f"\nError: {event.error}", file=sys.stderr)
                break
            elif isinstance(event, UnknownRealtimeEvent):
                # ignore future / unknown events; keep going
                continue

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
