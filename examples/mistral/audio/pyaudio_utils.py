from __future__ import annotations

from types import ModuleType


def load_pyaudio() -> ModuleType:
    """
    Import PyAudio with a friendly error when PortAudio is missing.

    Raises:
        RuntimeError: If PyAudio/PortAudio cannot be imported.
    """
    try:
        import pyaudio
    except Exception as exc:
        details = str(exc).lower()
        if isinstance(exc, ModuleNotFoundError) and exc.name == "pyaudio":
            message = (
                "PyAudio is required to use the microphone.\n"
                "Install PortAudio (eg. for macos: brew install portaudio), then "
                "reinstall PyAudio."
            )
        elif "pyaudio._portaudio" in details or "portaudio" in details:
            message = (
                "PyAudio is installed, but the PortAudio native library is missing or "
                "failed to load.\n"
                "Install PortAudio (eg. for macos: brew install portaudio), then "
                "reinstall PyAudio."
            )
        else:
            message = (
                "PyAudio is required to use the microphone, but it could not be "
                "imported.\n"
                "Install PortAudio (eg. for macos: brew install portaudio), then "
                "reinstall PyAudio."
            )
        raise RuntimeError(message) from exc
    return pyaudio
