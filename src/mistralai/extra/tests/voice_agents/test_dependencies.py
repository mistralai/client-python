"""Diagnostics for an optional dependency that is missing or fails to load."""
import builtins
import importlib
import sys
from unittest.mock import Mock

import pytest

from mistralai.extra.voice_agents import utils as utils_module
from mistralai.extra.voice_agents.errors import VoiceAgentDependencyError
from mistralai.extra.voice_agents.utils import _load_pyaudio

TRANSPORT_MODULE = "mistralai.extra.voice_agents.transport"


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (
            ModuleNotFoundError("No module named 'livekit'", name="livekit"),
            "pip install 'mistralai[voice-agents]'",
        ),
        (
            ImportError("DLL load failed while importing rtc", name="livekit"),
            "livekit: it is installed but failed to import",
        ),
    ],
    ids=["absent", "unloadable"],
)
def test_transport_import_failure_distinguishes_absent_from_unloadable(
    monkeypatch, error, expected
):
    real_import = builtins.__import__

    def fail_on_livekit(name, *args, **kwargs):
        if name.startswith("livekit"):
            raise error
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fail_on_livekit)
    monkeypatch.delitem(sys.modules, TRANSPORT_MODULE, raising=False)

    with pytest.raises(VoiceAgentDependencyError) as exc_info:
        importlib.import_module(TRANSPORT_MODULE)

    assert expected in str(exc_info.value)
    assert exc_info.value.__cause__ is error


@pytest.mark.parametrize(
    ("platform", "expected", "forbidden"),
    [
        ("darwin", "brew install portaudio", ("apt install",)),
        ("linux", "apt install portaudio19-dev", ("brew install",)),
        (
            "win32",
            'pip install "mistralai[voice-agents]"',
            ("brew install", "apt install", "PortAudio"),
        ),
    ],
)
def test_pyaudio_import_failure_hint_is_platform_aware(
    monkeypatch, platform, expected, forbidden
):
    monkeypatch.setattr(utils_module.sys, "platform", platform)
    monkeypatch.setattr(
        utils_module.importlib,
        "import_module",
        Mock(side_effect=ImportError("no pyaudio")),
    )

    with pytest.raises(VoiceAgentDependencyError) as exc_info:
        _load_pyaudio()

    message = str(exc_info.value)
    assert expected in message
    assert not any(text in message for text in forbidden)
    assert message == message.strip()
