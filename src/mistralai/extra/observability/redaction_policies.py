"""Redaction policies for client-side redaction of telemetry spans.

Can be customized through the CallRedactionPolicy, or be extended by subclassing
RedactionPolicy.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from typing import Callable, Final, cast

from opentelemetry.util.types import AttributeValue

# User-supplied per-attribute masker: given (key, value), return the value
# to keep. Return the value unchanged to keep it, a redacted value to mask it,
# or None to drop the attribute entirely
AttributeMaskCallback = Callable[[str, AttributeValue], AttributeValue | None]
DEFAULT_REDACTED_VALUE: Final[str] = "[REDACTED]"


def default_redaction_policy() -> RedactionPolicy:
    return RegexRedactionPolicy()


class RedactionPolicy(ABC):
    """Base class for redaction policies."""

    @abstractmethod
    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        """Return a new attribute mapping with sensitive data removed."""
        raise NotImplementedError

    def redact_span_name(self, name: str) -> str:
        """Return the span name to export. Defaults to unchanged."""
        return name

    def redact_status_description(self, description: str | None) -> str | None:
        """Return the status description to export. Defaults to unchanged."""
        return description


DEFAULT_SENSITIVE_ATTRIBUTE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "client.address",
        "db.query.text",
        "db.statement",
        "exception.message",
        "exception.stacktrace",
        "gen_ai.input.messages",
        "gen_ai.output.messages",
        "gen_ai.tool.definitions",
        "gen_ai.tool.call.arguments",
        "gen_ai.tool.call.result",
        "http.request.body",
        "http.request.header.authorization",
        "http.request.header.cookie",
        "http.response.body",
        "http.response.header.set-cookie",
        "http.target",
        "http.url",
        "server.address",
        "url.full",
        "url.path",
        "url.query",
    }
)
DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "argument",
        "arguments",
        "authorization",
        "body",
        "completion",
        "content",
        "cookie",
        "input",
        "message",
        "messages",
        "output",
        "password",
        "payload",
        "prompt",
        "secret",
        "set_cookie",
        "token",
    }
)
DEFAULT_SAFE_ATTRIBUTE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "agent.trace.public",
        "client.port",
        "error.type",
        "exception.type",
        "gen_ai.agent.name",
        "gen_ai.conversation.id",
        "gen_ai.operation.name",
        "gen_ai.provider.name",
        "gen_ai.request.model",
        "gen_ai.response.finish_reasons",
        "gen_ai.response.id",
        "gen_ai.response.model",
        "gen_ai.tool.call.id",
        "gen_ai.tool.name",
        "gen_ai.tool.type",
        "http.request.method",
        "http.response.status_code",
        "network.protocol.name",
        "network.protocol.version",
        "server.port",
        "url.scheme",
    }
)
DEFAULT_TOKEN_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"(?i)bearer\s+[a-z0-9._\-]+"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b[sr]k_(?:live|test)_[0-9A-Za-z]{10,}\b"),
    # AI providers
    re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{20,}\b"),
    re.compile(r"\bsk-proj-[A-Za-z0-9\-_]{20,}\b"),
    re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"),
    # Dev / infra tokens
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b"),
    re.compile(r"\bglpat-[A-Za-z0-9\-=_]{20,22}\b"),
    re.compile(r"\bshp(?:at|ca|pa|ss)_[a-fA-F0-9]{32}\b"),
    re.compile(r"\bsq0(?:atp|csp|idp)-[0-9A-Za-z\-_]{22,43}\b"),
    re.compile(r"\bPMAK-[a-zA-Z0-9]{24,59}\b"),
    re.compile(r"\bphc_[a-zA-Z0-9_]{43}\b"),
    re.compile(r"\brubygems_[a-f0-9]{48}\b"),
    re.compile(r"\blin_api_[0-9A-Za-z]{40}\b"),
    re.compile(r"pypi-AgEIcHlwaS5vcmc[A-Za-z0-9\-_]{50,}"),
    re.compile(r"\bsecret_[A-Za-z0-9]{43}\b"),
    re.compile(r"[A-Za-z0-9]{14}\.atlasv1\.[A-Za-z0-9]{60,}"),
    re.compile(r"\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b"),
    re.compile(r"\bpk_(?:live|test)_[0-9a-zA-Z]{24}\b"),
    # Webhook URLs (the whole URL is the secret)
    re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/+]{40,}"),
    re.compile(
        r"https://discord(?:app)?\.com/api/webhooks/[0-9]{17,}/[A-Za-z0-9\-_]{60,}"
    ),
    re.compile(r"https://hooks\.zapier\.com/hooks/catch/[A-Za-z0-9/]{16,}"),
)
_SAFE_KEY_PREFIXES: Final[tuple[str, ...]] = ("gen_ai.usage.",)
_PRIMITIVE_TYPES: Final[tuple[type, ...]] = (str, bool, int, float)


class AttributeRedactionPolicy(RedactionPolicy):
    """Key-oriented hybrid policy.

    An opt-in, high-recall alternative to the default policy: "safe by default", at the cost
    of erasing most prompt/response content. It redacts whole values for keys judged sensitive
    (explicit set, fragment match, or non-primitive value), then runs token_patterns over the
    values it keeps to redact values.

    When emit_redaction_metadata is enabled, each redaction emits a companion attribute.
    For a value removed wholesale: {key}.redacted_length for strings/bytes,
    {key}.redacted_count for collections, {key}.redacted_type otherwise. For matches scrubbed
    from a value that is otherwise kept: {key}.redacted_matches, the number of substitutions
    made (summed across sequence elements).
    """

    def __init__(
        self,
        *,
        sensitive_keys: frozenset[str] = DEFAULT_SENSITIVE_ATTRIBUTE_KEYS,
        safe_keys: frozenset[str] = DEFAULT_SAFE_ATTRIBUTE_KEYS,
        sensitive_fragments: frozenset[str] = DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS,
        token_patterns: Sequence[re.Pattern[str]] = DEFAULT_TOKEN_PATTERNS,
        redact_non_primitive: bool = True,
        redacted_value: str = DEFAULT_REDACTED_VALUE,
        emit_redaction_metadata: bool = False,
    ) -> None:
        self._sensitive_keys = sensitive_keys
        self._safe_keys = safe_keys
        self._sensitive_fragments = sensitive_fragments
        self._token_patterns = tuple(token_patterns)
        self._redact_non_primitive = redact_non_primitive
        self._redacted_value = redacted_value
        self._emit_redaction_metadata = emit_redaction_metadata

    def _should_redact(self, key: str, value: object) -> bool:
        normalized_key = key.lower()
        if normalized_key in self._safe_keys:
            return False
        if normalized_key.startswith(_SAFE_KEY_PREFIXES):
            return False
        if normalized_key in self._sensitive_keys:
            return True
        if self._has_sensitive_fragment(normalized_key):
            return True
        return self._redact_non_primitive and not isinstance(value, _PRIMITIVE_TYPES)

    def _has_sensitive_fragment(self, normalized_key: str) -> bool:
        normalized_words = normalized_key.replace("-", "_").replace(".", "_")
        key_fragments = {word for word in normalized_words.split("_") if word}
        return any(
            fragment in key_fragments or fragment in normalized_words
            for fragment in self._sensitive_fragments
        )

    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        redacted: dict[str, AttributeValue] = {}
        if attributes is None:
            return redacted

        for key, value in attributes.items():
            if self._emit_redaction_metadata and _is_redaction_metadata(key):
                redacted[key] = value
                continue
            if self._should_redact(key, value):
                redacted[key] = self._redacted_value
                if self._emit_redaction_metadata:
                    redacted.update(_redaction_metadata(key, value))
                continue
            if self._emit_redaction_metadata:
                kept_value, matches = _redact_value_counting(
                    value, self._token_patterns, self._redacted_value
                )
                redacted[key] = kept_value
                if matches:
                    redacted[f"{key}.redacted_matches"] = matches
                continue
            redacted[key] = _redact_value(
                value, self._token_patterns, self._redacted_value
            )

        return redacted

    def redact_status_description(self, description: str | None) -> str | None:
        """Redact error descriptions (they often carry request/response text)."""
        if description is None:
            return None
        return self._redacted_value


DEFAULT_PII_SECRET_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    *DEFAULT_TOKEN_PATTERNS,
    # Email addresses
    re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    # Credit-card-like sequences (13-16 digits, optional spaces/dashes)
    re.compile(r"\b(?:\d[ -]?){13,16}\b"),
    # IPv4 addresses
    re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
    ),
)


class RegexRedactionPolicy(RedactionPolicy):
    """Content-oriented policy based on regexes.

    This is the default policy. Leaves keys and structure intact, scans string values and
    redacts matched substrings. Fewer false positives than AttributeRedactionPolicy and aims
    to preserve observability value; may miss free-form PII or secrets not in the default
    patterns.
    """

    def __init__(
        self,
        patterns: Sequence[re.Pattern[str]] = DEFAULT_PII_SECRET_PATTERNS,
        *,
        redacted_value: str = DEFAULT_REDACTED_VALUE,
    ) -> None:
        self._patterns = tuple(patterns)
        self._redacted_value = redacted_value

    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        redacted: dict[str, AttributeValue] = {}
        if attributes is None:
            return redacted

        for key, value in attributes.items():
            redacted[key] = _redact_value(value, self._patterns, self._redacted_value)

        return redacted

    def redact_span_name(self, name: str) -> str:
        return _redact_text(name, self._patterns, self._redacted_value)

    def redact_status_description(self, description: str | None) -> str | None:
        if description is None:
            return None
        return _redact_text(description, self._patterns, self._redacted_value)


class CallbackRedactionPolicy(RedactionPolicy):
    """Callback-based policy for users to provide custom redaction capabilities.

    The callback is invoked per attribute and should return the value to keep or None to drop the attribute.
    Span name and status description are left unchanged (the callback operates on attributes only).
    """

    def __init__(self, mask_function: AttributeMaskCallback) -> None:
        self._mask_function = mask_function

    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        redacted: dict[str, AttributeValue] = {}
        if attributes is None:
            return redacted

        for key, value in attributes.items():
            masked = self._mask_function(key, value)
            if masked is None:
                continue
            redacted[key] = masked

        return redacted


def _redact_value(
    value: AttributeValue,
    patterns: Sequence[re.Pattern[str]],
    redacted_value: str = DEFAULT_REDACTED_VALUE,
) -> AttributeValue:
    redacted, _ = _redact_value_counting(value, patterns, redacted_value)
    return redacted


def _redact_value_counting(
    value: AttributeValue,
    patterns: Sequence[re.Pattern[str]],
    redacted_value: str = DEFAULT_REDACTED_VALUE,
) -> tuple[AttributeValue, int]:
    if isinstance(value, str):
        return _redact_text_counting(value, patterns, redacted_value)
    if isinstance(value, (list, tuple)):
        total = 0
        items: list[AttributeValue] = []
        for item in value:
            if isinstance(item, str):
                redacted_item, count = _redact_text_counting(
                    item, patterns, redacted_value
                )
                total += count
                items.append(redacted_item)
            else:
                items.append(item)
        result = tuple(items) if isinstance(value, tuple) else items
        return cast(AttributeValue, result), total
    return value, 0


def _redact_text(
    text: str,
    patterns: Sequence[re.Pattern[str]],
    redacted_value: str = DEFAULT_REDACTED_VALUE,
) -> str:
    redacted, _ = _redact_text_counting(text, patterns, redacted_value)
    return redacted


def _redact_text_counting(
    text: str,
    patterns: Sequence[re.Pattern[str]],
    redacted_value: str = DEFAULT_REDACTED_VALUE,
) -> tuple[str, int]:
    redacted = text
    total = 0
    for pattern in patterns:
        redacted, count = pattern.subn(redacted_value, redacted)
        total += count
    return redacted, total


_REDACTION_METADATA_SUFFIXES: Final[tuple[str, ...]] = (
    ".redacted_count",
    ".redacted_length",
    ".redacted_matches",
    ".redacted_type",
)


def _is_redaction_metadata(key: str) -> bool:
    return key.lower().endswith(_REDACTION_METADATA_SUFFIXES)


def _redaction_metadata(key: str, value: object) -> dict[str, AttributeValue]:
    if isinstance(value, (str, bytes, bytearray)):
        return {f"{key}.redacted_length": len(value)}
    if isinstance(value, Mapping):
        return {f"{key}.redacted_count": len(value)}
    if isinstance(value, Sequence):
        return {f"{key}.redacted_count": len(value)}
    return {f"{key}.redacted_type": type(value).__name__}
