#!/usr/bin/env python3
"""Minimal local smoke test for /v1/audio/speech stream overload behavior.

Run:
    uv run python scripts/speech_sse_smoke.py
or:
    uvx --from . python scripts/speech_sse_smoke.py
"""

from __future__ import annotations

import json

import httpx

from mistralai.client import Mistral, models


def _sse_bytes() -> bytes:
    """Return two SSE events: one delta and one done."""
    events = [
        "event: speech.audio.delta\n"
        'data: {"type":"speech.audio.delta","audio_data":"Zm9v"}\n\n',
        "event: speech.audio.done\n"
        'data: {"type":"speech.audio.done","usage":{"prompt_tokens":1,"total_tokens":1}}\n\n',
    ]
    return "".join(events).encode("utf-8")


def _handler(request: httpx.Request) -> httpx.Response:
    assert request.method == "POST"
    assert request.url.path == "/v1/audio/speech"

    accept = request.headers.get("accept")
    payload = json.loads(request.content.decode("utf-8"))
    stream = bool(payload.get("stream", False))

    if stream:
        assert accept == "text/event-stream", f"unexpected accept={accept}"
        return httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content=_sse_bytes(),
            request=request,
        )

    assert accept == "application/json", f"unexpected accept={accept}"
    return httpx.Response(
        200,
        headers={"content-type": "application/json"},
        json={"audio_data": "Zm9v"},
        request=request,
    )


def main() -> None:
    transport = httpx.MockTransport(_handler)
    client = httpx.Client(transport=transport, base_url="https://api.mistral.ai")

    sdk = Mistral(api_key="dummy", client=client)

    non_stream = sdk.audio.speech.complete(input="hello", stream=False)
    assert isinstance(non_stream, models.SpeechResponse)
    assert isinstance(non_stream.audio_data, (bytes, bytearray))
    print(f"stream=False OK: {type(non_stream).__name__}")

    stream_resp = sdk.audio.speech.complete(input="hello", stream=True)
    assert hasattr(stream_resp, "__iter__")

    collected: list[models.SpeechStreamEvents] = list(
        stream_resp  # type: ignore[arg-type]
    )
    assert len(collected) == 2
    assert collected[0].event == "speech.audio.delta"
    assert collected[1].event == "speech.audio.done"

    print("stream=True OK: received events ->", [event.event for event in collected])
    print("All good.")


if __name__ == "__main__":
    main()
