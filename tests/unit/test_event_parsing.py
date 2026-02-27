"""Tests for _parse_event() and related constants in eventstreaming module."""

import json

import pytest

from mistralai.client.utils.eventstreaming import (
    MESSAGE_BOUNDARIES,
    UTF8_BOM,
    ServerEvent,
    _parse_event,
)


def _identity_decoder(raw: str):
    """Decode a JSON string into a dict."""
    return json.loads(raw)


# -------------------------------------------------------------------------
# 1. Data field parsed
# -------------------------------------------------------------------------


class TestDataFieldParsed:
    def test_data_field_parsed(self):
        raw = bytearray(b"data: {\"key\": \"value\"}")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is not None
        assert result["data"] == {"key": "value"}
        assert discard is False
        assert eid is None


# -------------------------------------------------------------------------
# 2. Event field
# -------------------------------------------------------------------------


class TestEventField:
    def test_event_field(self):
        raw = bytearray(b"event: foo\ndata: {}")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is not None
        assert result["event"] == "foo"
        assert result["data"] == {}
        assert discard is False


# -------------------------------------------------------------------------
# 3. Id field
# -------------------------------------------------------------------------


class TestIdField:
    def test_id_field(self):
        raw = bytearray(b"id: 42\ndata: {}")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is not None
        assert result["id"] == "42"
        assert eid == "42"


# -------------------------------------------------------------------------
# 4. Retry field
# -------------------------------------------------------------------------


class TestRetryField:
    def test_retry_field(self):
        raw = bytearray(b"retry: 5000\ndata: {}")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is not None
        assert result["retry"] == 5000
        assert result["data"] == {}


# -------------------------------------------------------------------------
# 5. Multi data lines
# -------------------------------------------------------------------------


class TestMultiDataLines:
    def test_multi_data_lines(self):
        raw = bytearray(b"data: line1\ndata: line2")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is not None
        # Two data lines are concatenated with \n separator
        assert result["data"] == "line1\nline2"


# -------------------------------------------------------------------------
# 6. Sentinel detection
# -------------------------------------------------------------------------


class TestSentinelDetection:
    def test_sentinel_detection(self):
        raw = bytearray(b"data: [DONE]")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder, sentinel="[DONE]"
        )
        assert result is None
        assert discard is True

    def test_sentinel_with_event_id_carried(self):
        raw = bytearray(b"data: [DONE]")
        result, discard, eid = _parse_event(
            raw=raw,
            decoder=_identity_decoder,
            sentinel="[DONE]",
            event_id="prev-id",
        )
        assert result is None
        assert discard is True
        assert eid == "prev-id"


# -------------------------------------------------------------------------
# 7. Comment lines ignored
# -------------------------------------------------------------------------


class TestCommentLinesIgnored:
    def test_comment_lines_ignored(self):
        raw = bytearray(b": this is a comment\ndata: {\"ok\": true}")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is not None
        assert result["data"] == {"ok": True}


# -------------------------------------------------------------------------
# 8. Empty block
# -------------------------------------------------------------------------


class TestEmptyBlock:
    def test_empty_block(self):
        raw = bytearray(b"")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is None
        assert discard is False
        assert eid is None


# -------------------------------------------------------------------------
# 9. JSON decode failure falls back to raw string
# -------------------------------------------------------------------------


class TestJsonDecodeFailureRawString:
    def test_json_decode_failure_raw_string(self):
        raw = bytearray(b"data: this is not json")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        # The data field should contain the raw string since JSON parsing fails.
        # The decoder receives a JSON-serialized dict containing the raw string
        # as the data value, so it should parse fine at the decoder level.
        assert result is not None
        assert result["data"] == "this is not json"


# -------------------------------------------------------------------------
# 10. All message boundaries exist
# -------------------------------------------------------------------------


class TestAllMessageBoundariesExist:
    def test_all_message_boundaries_exist(self):
        assert len(MESSAGE_BOUNDARIES) == 8
        assert isinstance(MESSAGE_BOUNDARIES, list)
        for boundary in MESSAGE_BOUNDARIES:
            assert isinstance(boundary, bytes)


# -------------------------------------------------------------------------
# 11. UTF8 BOM constant
# -------------------------------------------------------------------------


class TestUtf8BomConstant:
    def test_utf8_bom_constant(self):
        assert UTF8_BOM == b"\xef\xbb\xbf"


# -------------------------------------------------------------------------
# 12. Id with null char not updated
# -------------------------------------------------------------------------


class TestIdWithNullCharNotUpdated:
    def test_id_with_null_char_not_updated(self):
        raw = bytearray(b"id: abc\x00def\ndata: {}")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        # id containing \x00 must not update event_id
        assert eid is None
        assert result is not None

    def test_id_with_null_char_preserves_previous_event_id(self):
        raw = bytearray(b"id: abc\x00def\ndata: {}")
        result, discard, eid = _parse_event(
            raw=raw,
            decoder=_identity_decoder,
            event_id="old-id",
        )
        # The previous event_id should be preserved, not overwritten
        assert eid == "old-id"


# -------------------------------------------------------------------------
# 13. Field without value (no colon)
# -------------------------------------------------------------------------


class TestFieldWithoutValue:
    def test_field_without_value(self):
        # A line like "data" (no colon) is treated as field with empty value
        raw = bytearray(b"data\ndata: actual")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is not None
        # "data" (no colon) produces empty string, "data: actual" produces
        # "actual", both concatenated with \n
        assert result["data"] == "\nactual"


# -------------------------------------------------------------------------
# 14. Value with leading space stripped
# -------------------------------------------------------------------------


class TestValueWithLeadingSpaceStripped:
    def test_value_with_leading_space_stripped(self):
        raw = bytearray(b"data: hello")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is not None
        assert result["data"] == "hello"

    def test_value_without_leading_space_preserved(self):
        raw = bytearray(b"data:hello")
        result, discard, eid = _parse_event(
            raw=raw, decoder=_identity_decoder
        )
        assert result is not None
        assert result["data"] == "hello"


# -------------------------------------------------------------------------
# 15. Event id persistence
# -------------------------------------------------------------------------


class TestEventIdPersistence:
    def test_event_id_persistence(self):
        # First parse sets event_id
        raw1 = bytearray(b"id: ev-1\ndata: {}")
        result1, _, eid1 = _parse_event(
            raw=raw1, decoder=_identity_decoder
        )
        assert eid1 == "ev-1"

        # Second parse carries through the event_id from previous call
        raw2 = bytearray(b"data: {}")
        result2, _, eid2 = _parse_event(
            raw=raw2, decoder=_identity_decoder, event_id=eid1
        )
        assert result2 is not None
        assert result2["id"] == "ev-1"
        assert eid2 == "ev-1"
