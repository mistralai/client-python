from __future__ import annotations

import asyncio
import sys
import threading
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Callable, Mapping
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from livekit import rtc

from .errors import VoiceAgentConnectionError
from .utils import _load_pyaudio

_Direction = Literal["input", "output"]
_StreamCallback = Callable[
    [bytes | None, int, Mapping[str, float], int], tuple[bytes | None, int]
]

CHANNELS = 1
SAMPLE_RATE = 48_000
FRAME_DURATION_MS = 20
BYTES_PER_SAMPLE = 2


class AudioInterface(ABC):
    async def preflight(self) -> None:
        """Check local preconditions for `start()` before the session is created."""

    @abstractmethod
    async def start(self) -> None:
        """Open local devices, sockets, or other audio resources."""

    @abstractmethod
    def input_audio(self) -> AsyncIterator[bytes]:
        """Yield user audio bytes that should be sent to the voice agent."""

    @abstractmethod
    async def output_audio(self, audio: bytes) -> None:
        """Receive agent audio bytes for local playback or forwarding."""

    @abstractmethod
    async def stop(self) -> None:
        """Close local devices, sockets, or other audio resources."""


class DefaultAudioInterface(AudioInterface):
    """PyAudio-backed microphone and speaker interface."""

    def __init__(
        self,
        *,
        frames_per_buffer: int | None = None,
        output_buffer_size_ms: int = 300,
        echo_cancellation: bool = True,
        noise_suppression: bool = True,
        high_pass_filter: bool = True,
        auto_gain_control: bool = True,
        echo_cancellation_delay_ms: int | None = None,
    ) -> None:
        self._frames_per_buffer = frames_per_buffer or (
            SAMPLE_RATE * FRAME_DURATION_MS // 1000
        )
        self._output_frame_width = CHANNELS * BYTES_PER_SAMPLE
        self._output_buffer_max_bytes = (
            SAMPLE_RATE * self._output_frame_width * output_buffer_size_ms // 1000
        )
        self._output_buffer_max_bytes = _align_byte_count(
            max(self._output_frame_width, self._output_buffer_max_bytes),
            self._output_frame_width,
        )
        self._output_buffer = bytearray()
        self._output_buffer_lock = threading.Lock()
        self._echo_cancellation = echo_cancellation
        self._noise_suppression = noise_suppression
        self._high_pass_filter = high_pass_filter
        self._auto_gain_control = auto_gain_control
        self._echo_cancellation_delay_ms = echo_cancellation_delay_ms
        self._apm_lock = threading.Lock()
        self._last_output_delay_ms = 0
        self._pyaudio_module: Any = None
        self._pyaudio: Any = None
        self._audio_processing_module: rtc.AudioProcessingModule | None = None
        self._input_processor: _AudioFrameProcessor | None = None
        self._output_processor: _AudioFrameProcessor | None = None
        self._input_stream: Any | None = None
        self._output_stream: Any | None = None
        self._running = False

    async def preflight(self) -> None:
        _load_pyaudio()

    async def start(self) -> None:
        if self._running:
            raise VoiceAgentConnectionError(
                "Default audio interface is already running"
            )
        pyaudio_module = _load_pyaudio()
        self._pyaudio_module = pyaudio_module
        self._configure_audio_processing()
        try:
            pyaudio = pyaudio_module.PyAudio()
        except OSError as exc:
            raise VoiceAgentConnectionError(
                f"Failed to initialize system audio: {exc}"
            ) from exc
        self._pyaudio = pyaudio
        self._running = True
        self._input_stream = await self._open_stream(direction="input", callback=None)
        self._output_stream = await self._open_stream(
            direction="output", callback=self._output_callback
        )

    async def _open_stream(
        self, *, direction: _Direction, callback: _StreamCallback | None
    ) -> Any:
        try:
            return self._pyaudio.open(
                format=self._pyaudio_module.paInt16,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=direction == "input",
                output=direction == "output",
                frames_per_buffer=self._frames_per_buffer,
                stream_callback=callback,
            )
        except OSError as exc:
            await self.stop()
            raise _audio_device_error(exc, direction=direction) from exc

    def input_audio(self) -> AsyncIterator[bytes]:
        return self._read_input()

    async def output_audio(self, audio: bytes) -> None:
        if not self._running:
            return
        stream = self._output_stream
        try:
            output_is_active = stream is not None and stream.is_active()
        except OSError as exc:
            raise VoiceAgentConnectionError(
                f"The default audio output device became unavailable: {exc}"
            ) from exc
        if not output_is_active:
            raise VoiceAgentConnectionError(
                "The default audio output device is unavailable"
            )
        with self._output_buffer_lock:
            self._output_buffer.extend(audio)
            overflow = len(self._output_buffer) - self._output_buffer_max_bytes
            if overflow > 0:
                aligned_overflow = _align_byte_count(
                    overflow,
                    self._output_frame_width,
                )
                del self._output_buffer[:aligned_overflow]

    async def stop(self) -> None:
        self._running = False
        with self._output_buffer_lock:
            self._output_buffer.clear()
        for stream in (self._input_stream, self._output_stream):
            if stream is None:
                continue
            await asyncio.to_thread(_close_stream, stream)
        self._input_stream = None
        self._output_stream = None
        with self._apm_lock:
            self._audio_processing_module = None
            self._input_processor = None
            self._output_processor = None
        if self._pyaudio is not None:
            await asyncio.to_thread(self._pyaudio.terminate)
        self._pyaudio = None

    async def _read_input(self) -> AsyncIterator[bytes]:
        while self._running:
            stream = self._input_stream
            if stream is None:
                return
            try:
                data = await asyncio.to_thread(
                    stream.read,
                    self._frames_per_buffer,
                    exception_on_overflow=False,
                )
            except OSError as exc:
                raise VoiceAgentConnectionError(
                    f"The default audio input device became unavailable: {exc}"
                ) from exc
            processed = self._process_input_audio(bytes(data))
            if not processed:
                continue
            yield processed

    def _output_callback(
        self,
        _input_data: bytes | None,
        frame_count: int,
        _time_info: Mapping[str, float],
        _status_flags: int,
    ) -> tuple[bytes, int]:
        pyaudio_module = self._pyaudio_module
        byte_count = frame_count * self._output_frame_width
        with self._output_buffer_lock:
            data = bytes(self._output_buffer[:byte_count])
            del self._output_buffer[:byte_count]

        if len(data) < byte_count:
            data += b"\x00" * (byte_count - len(data))

        self._process_output_audio(data, time_info=_time_info)
        flag = pyaudio_module.paContinue if self._running else pyaudio_module.paComplete
        return data, flag

    def _configure_audio_processing(self) -> None:
        if not (
            self._echo_cancellation
            or self._noise_suppression
            or self._high_pass_filter
            or self._auto_gain_control
        ):
            return

        from livekit import rtc

        apm = rtc.AudioProcessingModule(
            echo_cancellation=self._echo_cancellation,
            noise_suppression=self._noise_suppression,
            high_pass_filter=self._high_pass_filter,
            auto_gain_control=self._auto_gain_control,
        )
        self._audio_processing_module = apm
        self._input_processor = _AudioFrameProcessor(
            process_frame=apm.process_stream,
            lock=self._apm_lock,
        )
        if self._echo_cancellation:
            self._output_processor = _AudioFrameProcessor(
                process_frame=apm.process_reverse_stream,
                lock=self._apm_lock,
            )

    def _process_input_audio(self, data: bytes) -> bytes:
        apm = self._audio_processing_module
        processor = self._input_processor
        if apm is None or processor is None:
            return data

        if self._echo_cancellation:
            with self._apm_lock:
                apm.set_stream_delay_ms(self._current_echo_delay_ms())
        return processor.push(data)

    def _process_output_audio(
        self, data: bytes, *, time_info: Mapping[str, float]
    ) -> None:
        processor = self._output_processor
        if processor is None:
            return

        self._last_output_delay_ms = _output_delay_ms(time_info)
        processor.push(data)

    def _current_echo_delay_ms(self) -> int:
        if self._echo_cancellation_delay_ms is not None:
            return self._echo_cancellation_delay_ms
        input_buffer_delay_ms = self._frames_per_buffer * 1000 // SAMPLE_RATE
        return max(input_buffer_delay_ms + self._last_output_delay_ms, 0)


class _AudioFrameProcessor:
    def __init__(
        self,
        *,
        process_frame: Callable[[rtc.AudioFrame], None],
        lock: threading.Lock,
    ) -> None:
        self._samples_per_channel = SAMPLE_RATE // 100
        self._frame_byte_count = self._samples_per_channel * CHANNELS * BYTES_PER_SAMPLE
        self._process_frame = process_frame
        self._lock = lock
        self._pending = bytearray()

    def push(self, data: bytes) -> bytes:
        self._pending.extend(data)
        processed = bytearray()

        while len(self._pending) >= self._frame_byte_count:
            frame_data = self._pending[: self._frame_byte_count]
            del self._pending[: self._frame_byte_count]
            from livekit import rtc

            frame = rtc.AudioFrame(
                data=bytearray(frame_data),
                sample_rate=SAMPLE_RATE,
                num_channels=CHANNELS,
                samples_per_channel=self._samples_per_channel,
            )
            with self._lock:
                self._process_frame(frame)
            processed.extend(frame.data.tobytes())

        return bytes(processed)


_PORTAUDIO_HINTS: dict[int | None, str] = {
    -9996: "no {noun} is available — connect one and retry",
    -9985: (
        "the {noun} is held by another application — close whatever else is "
        "using it and retry"
    ),
    -9998: "the {noun} does not support single-channel audio",
    -9997: "the {noun} does not support a 48 kHz sample rate",
    -9999: (
        "the {noun} rejected the request — another application may hold it in "
        "exclusive mode, or it may not support the requested format"
    ),
}

_MIC_PERMISSION_PATHS = {
    "darwin": "System Settings → Privacy & Security → Microphone",
    "win32": "Settings → Privacy & security → Microphone",
}


def _audio_device_error(
    exc: OSError,
    *,
    direction: _Direction,
) -> VoiceAgentConnectionError:
    noun = "microphone" if direction == "input" else "speaker"
    hint = _PORTAUDIO_HINTS.get(exc.errno)
    permission_path = _MIC_PERMISSION_PATHS.get(sys.platform)
    if hint is not None:
        hint = hint.format(noun=noun)
    elif direction == "input" and permission_path is not None:
        hint = (
            "the microphone could not be opened — the operating system may not "
            f"have granted access; allow it under {permission_path}, then rerun"
        )
    else:
        hint = f"the default {noun} could not be opened"
    return VoiceAgentConnectionError(f"{hint}. Underlying audio error: {exc}")


def _close_stream(stream: Any) -> None:
    try:
        if hasattr(stream, "stop_stream"):
            stream.stop_stream()
    finally:
        if hasattr(stream, "close"):
            stream.close()


def _align_byte_count(byte_count: int, frame_width: int) -> int:
    return ((byte_count + frame_width - 1) // frame_width) * frame_width


def _output_delay_ms(time_info: Mapping[str, float]) -> int:
    current_time = time_info.get("current_time")
    output_time = time_info.get("output_buffer_dac_time")
    if current_time is None or output_time is None:
        return 0
    return max(int((output_time - current_time) * 1000), 0)
