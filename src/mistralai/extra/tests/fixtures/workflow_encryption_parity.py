"""Shared fixtures for workflow payload encryption parity with the TS client.

The TypeScript client (``ts/client-ts``) must produce the same encrypted bytes
as this client. These cases run the real ``PayloadEncoder`` with deterministic
nonces and are written to the TS test suite, which replays them. The
``test_workflow_encryption_parity`` test checks that this client still
produces the committed file.

Regenerate the file from ``client-python`` with:

    uv run python -m mistralai.extra.tests.fixtures.workflow_encryption_parity
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Iterator
from unittest import mock

from pydantic import SecretStr

from mistralai.extra.workflows.encoding import (
    PayloadEncryptionConfig,
    PayloadEncryptionMode,
    WorkflowEncodingConfig,
)
from mistralai.extra.workflows.encoding import payload_encoder as payload_encoder_module
from mistralai.extra.workflows.encoding.models import (
    EncodedPayloadOptions,
    WorkflowContext,
)
from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder

FIXTURE_PATH = (
    Path(__file__).resolve().parents[6]
    / "ts"
    / "client-ts"
    / "tests"
    / "extra"
    / "fixtures"
    / "workflow_encryption_parity.json"
)


def _hex_key(seed: str, size: int = 32) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()[: size * 2]


KEYS = {
    "main": _hex_key("main-key"),
    "secondary": _hex_key("secondary-key"),
    "aes128": _hex_key("aes128-key", 16),
    "aes192": _hex_key("aes192-key", 24),
}


def _encrypted(data: str) -> dict[str, str]:
    return {"field_type": "__encrypted_str__", "data": data}


# Workflow inputs, as the workflow encoding hook receives them after parsing
# the request body. Integer-valued floats are left out: JavaScript can't tell
# them apart from integers (the raw payload cases cover them).
NETWORK_INPUTS: dict[str, Any] = {
    "object": {"name": "alice", "count": 3, "active": True, "tags": ["a", "b"]},
    "nested": {"a": {"b": {"c": [1, {"d": None}, [], {}]}}, "z": False},
    "unicode": {"text": "héllo wörld ✓ 😀 \u2028", "ctrl": "\x00\x1f\x7f\n\t\"\\/"},
    "numbers": {
        "floats": [0.5, -1.25, 0.1, 1e-05, 1.5e-06, 1e-07, 123456.789, 1e-300],
        "ints": [0, -7, 9007199254740991, 1000000000000000000000],
        "tiny": 5e-324,
    },
    # JavaScript objects always list integer-like keys first, in ascending
    # order, so a JS input can only have this order (raw payloads cover others).
    "integer_like_keys": {"2": "two", "10": "ten", "b": 1, "a": 2},
    "string": "just a string",
    "list": [1, "two", {"three": 3}],
    "number": 42,
    "empty_object": {},
    "partial_top_level": {
        "user": "alice",
        "api_key": _encrypted("sk-secret"),
        "unicode": _encrypted("mot de passe: été 😀"),
    },
    "partial_nested": {
        "config": {
            "credentials": [
                _encrypted("first"),
                {"inner": _encrypted("second"), "plain": "visible"},
            ],
            "empty": _encrypted(""),
        },
        "list": [[_encrypted("deep")]],
        # A marker stops the traversal: nested markers are data, not fields.
        "outer": {
            "field_type": "__encrypted_str__",
            "data": "outer",
            "extra": _encrypted("not-a-field"),
        },
    },
}

# Raw payload bytes given to ``encode_payload_content``. They exercise the
# re-serialization done by partial encryption with inputs that don't come
# from a serializer: whitespace, key order, duplicate keys, number formats.
RAW_PAYLOADS: dict[str, str] = {
    "numbers_and_whitespace": (
        ' {"b" : 2.0, "a":[1e5, 1E-7, -0, -0.0, 1.50, 12345678901234567890123,'
        ' 1e400, NaN, -Infinity], "10": 1, "2": {"field_type": "__encrypted_str__",'
        ' "data": "x"}}\n'
    ),
    "duplicate_keys": '{"k": 1, "j": 2, "k": {"field_type": "__encrypted_str__", "data": "v"}}',
    "escapes": r'{"s": "é😀\/\b\f", "e": {"field_type": "__encrypted_str__", "data": "\u0000"}}',
    "no_encrypted_fields": '{"a":1,"b":[true,false,null]}',
    "not_json": "this is not json",
}


def _nonces(case: str, count: int) -> list[str]:
    return [
        hashlib.sha256(f"{case}-nonce-{i}".encode()).hexdigest()[:24]
        for i in range(count)
    ]


def _encoder(mode: str, main: str, secondary: str | None = None) -> PayloadEncoder:
    return PayloadEncoder(
        WorkflowEncodingConfig(
            payload_encryption=PayloadEncryptionConfig(
                mode=PayloadEncryptionMode(mode),
                main_key=SecretStr(KEYS[main]),
                secondary_key=SecretStr(KEYS[secondary]) if secondary else None,
            )
        )
    )


def _config(mode: str, main: str, secondary: str | None = None) -> dict[str, Any]:
    config: dict[str, Any] = {"mode": mode, "main_key": main}
    if secondary:
        config["secondary_key"] = secondary
    return config


class _NonceQueue:
    """Feeds ``os.urandom`` with the nonces of the case being generated."""

    def __init__(self, case: str) -> None:
        self._nonces: Iterator[str] = iter(_nonces(case, 64))
        self.used: list[str] = []

    def __call__(self, size: int) -> bytes:
        assert size == PayloadEncoder._NONCE_SIZE
        nonce = next(self._nonces)
        self.used.append(nonce)
        return bytes.fromhex(nonce)


_CONTEXT = WorkflowContext(namespace="parity", execution_id="parity-execution")


def _run_with_nonces(case: str, fn: Callable[[], Any]) -> tuple[Any, list[str]]:
    """Runs ``fn`` (awaiting it if it returns a coroutine) with the case's nonces."""
    queue = _NonceQueue(case)
    with mock.patch.object(payload_encoder_module.os, "urandom", queue):
        result = fn()
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)
    return result, queue.used


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def _encode_network_input_cases() -> list[dict[str, Any]]:
    cases = []
    for mode, main in [("full", "main"), ("partial", "main"), ("full", "aes128"), ("full", "aes192")]:
        for input_name, input_value in NETWORK_INPUTS.items():
            if main != "main" and input_name not in ("object", "partial_top_level"):
                continue
            name = f"{mode}/{main}/{input_name}"
            encoder = _encoder(mode, main)
            encoded, nonces = _run_with_nonces(
                name, lambda: encoder.encode_network_input(input_value, _CONTEXT)
            )
            cases.append(
                {
                    "name": name,
                    "config": _config(mode, main),
                    "input": input_value,
                    "nonces": nonces,
                    "expected": encoded.model_dump(mode="json"),
                }
            )
    return cases


def _encode_payload_content_cases() -> list[dict[str, Any]]:
    cases = []
    for mode in ["partial", "full"]:
        for payload_name, payload in RAW_PAYLOADS.items():
            name = f"{mode}/{payload_name}"
            encoder = _encoder(mode, "main")
            (data, options), nonces = _run_with_nonces(
                name, lambda: encoder.encode_payload_content(payload.encode())
            )
            cases.append(
                {
                    "name": name,
                    "config": _config(mode, "main"),
                    "data_b64": _b64(payload.encode()),
                    "nonces": nonces,
                    "expected": {
                        "data_b64": _b64(data),
                        "encoding_options": [o.value for o in options],
                    },
                }
            )
    return cases


def _decode_network_result_cases() -> list[dict[str, Any]]:
    """Payloads encrypted with the secondary key, decoded after key rotation."""
    cases = []
    for mode in ["full", "partial"]:
        for input_name in ["object", "unicode", "partial_nested"]:
            name = f"{mode}/rotated/{input_name}"
            encoded, _ = _run_with_nonces(
                name,
                lambda: _encoder(mode, "secondary").encode_network_input(
                    NETWORK_INPUTS[input_name], _CONTEXT
                ),
            )
            decoder = _encoder(mode, "main", "secondary")
            expected = asyncio.run(
                decoder.decode_network_result(encoded.model_dump(mode="json"))
            )
            cases.append(
                {
                    "name": name,
                    "config": _config(mode, "main", "secondary"),
                    "encoded": encoded.model_dump(mode="json"),
                    "expected": expected,
                }
            )
    return cases


def _decode_event_payload_cases() -> list[dict[str, Any]]:
    encoder = _encoder("full", "main")

    def encrypt(value: Any, case: str) -> str:
        encrypted, _ = _run_with_nonces(
            case, lambda: encoder._encrypt(json.dumps(value).encode())
        )
        return _b64(encrypted)

    payloads: dict[str, dict[str, Any]] = {
        "json_full": {
            "type": "json",
            "value": encrypt({"state": "running", "progress": 0.5}, "json_full"),
            "encoding_options": [EncodedPayloadOptions.ENCRYPTED.value],
        },
        "json_patch_partial": {
            "type": "json_patch",
            "value": [
                {
                    "op": "add",
                    "path": "/secret",
                    "value": {
                        "type": "__encrypted__",
                        "value": encrypt({"token": "t0k3n"}, "patch-0"),
                    },
                },
                {"op": "replace", "path": "/plain", "value": "visible"},
                {
                    "op": "append",
                    "path": "/log",
                    "value": {
                        "type": "__encrypted__",
                        "value": encrypt("line ✓", "patch-1"),
                    },
                },
            ],
            "encoding_options": [EncodedPayloadOptions.PARTIALLY_ENCRYPTED.value],
        },
        "not_encoded": {"type": "json", "value": {"a": 1}, "encoding_options": []},
    }

    cases = []
    for name, payload in payloads.items():
        mode = "partial" if name == "json_patch_partial" else "full"
        expected = asyncio.run(
            _encoder(mode, "main").decode_event_payload(json.loads(json.dumps(payload)))
        )
        cases.append(
            {
                "name": name,
                "config": _config(mode, "main"),
                "payload": payload,
                "expected": expected,
            }
        )
    return cases


def build_fixtures() -> dict[str, Any]:
    return {
        "keys": KEYS,
        "encode_network_input": _encode_network_input_cases(),
        "encode_payload_content": _encode_payload_content_cases(),
        "decode_network_result": _decode_network_result_cases(),
        "decode_event_payload": _decode_event_payload_cases(),
    }


def render_fixtures() -> str:
    return json.dumps(build_fixtures(), indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(render_fixtures(), encoding="utf-8")
    print(f"Wrote {FIXTURE_PATH}")
