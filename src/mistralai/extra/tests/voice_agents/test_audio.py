import pytest

from mistralai.extra.voice_agents import audio as audio_module
from mistralai.extra.voice_agents.audio import _audio_device_error


@pytest.mark.parametrize(
    ("errno", "direction", "platform", "expected"),
    [
        (-9996, "input", "darwin", "no microphone is available"),
        (-9996, "output", "linux", "no speaker is available"),
        (-9985, "input", "linux", "held by another application"),
        (-9998, "output", "linux", "does not support single-channel audio"),
        (-9997, "input", "linux", "does not support a 48 kHz sample rate"),
        (-9999, "input", "win32", "another application may hold it in exclusive mode"),
        (-9986, "input", "darwin", "System Settings → Privacy & Security → Microphone"),
        (-9986, "input", "win32", "Settings → Privacy & security → Microphone"),
        (-9986, "input", "linux", "the default microphone could not be opened"),
        (-9986, "output", "darwin", "the default speaker could not be opened"),
    ],
)
def test_audio_device_error_explains_portaudio_codes(
    monkeypatch, errno, direction, platform, expected
):
    monkeypatch.setattr(audio_module.sys, "platform", platform)

    error = _audio_device_error(
        OSError(errno, "Unanticipated host error"), direction=direction
    )

    assert expected in str(error)
    assert "Unanticipated host error" in str(error)
