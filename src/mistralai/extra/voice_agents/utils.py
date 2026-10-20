from __future__ import annotations

import importlib
import json
import sys
from typing import Any

from .errors import VoiceAgentDependencyError

_PORTAUDIO_INSTALL_HINTS = {
    "darwin": "PortAudio must also be installed: `brew install portaudio`.",
    "linux": "PortAudio must also be installed: `apt install portaudio19-dev`.",
    "win32": "",
}
_DEFAULT_PORTAUDIO_INSTALL_HINT = (
    "PortAudio must also be installed "
    "(e.g. `brew install portaudio` / `apt install portaudio19-dev`)."
)


def _load_pyaudio() -> Any:
    try:
        return importlib.import_module("pyaudio")
    except Exception as exc:
        hint = _PORTAUDIO_INSTALL_HINTS.get(
            sys.platform, _DEFAULT_PORTAUDIO_INSTALL_HINT
        )
        raise VoiceAgentDependencyError(
            "PyAudio failed to import, install the voice-agents extra "
            f'(`pip install "mistralai[voice-agents]"`). {hint}'.strip()
        ) from exc


def _decode_json_payload(data: Any) -> Any:
    if isinstance(data, (bytes, bytearray, memoryview)):
        data = bytes(data).decode("utf-8", errors="replace")
    if not isinstance(data, str):
        return data
    try:
        return json.loads(data)
    except Exception:
        return data


def _optional_attr(obj: Any, name: str) -> str | None:
    if obj is None:
        return None
    value = getattr(obj, name, None)
    return value if isinstance(value, str) and value else None
