from typing import cast

import pytest
from opentelemetry.util.types import AttributeValue

from mistralai.extra.observability.redaction_policies import (
    DEFAULT_REDACTED_VALUE,
    AttributeRedactionPolicy,
    CallbackRedactionPolicy,
    RegexRedactionPolicy,
)


@pytest.fixture
def attribute_policy() -> AttributeRedactionPolicy:
    return AttributeRedactionPolicy()


@pytest.fixture
def regex_policy() -> RegexRedactionPolicy:
    return RegexRedactionPolicy()


class TestAttributeRedactionPolicy:
    def test_sensitive_key_redacted_wholesale(
        self, attribute_policy: AttributeRedactionPolicy
    ):
        out = attribute_policy.redact_attributes({"gen_ai.input.messages": "hello"})
        assert out["gen_ai.input.messages"] == DEFAULT_REDACTED_VALUE

    def test_safe_key_kept(self, attribute_policy: AttributeRedactionPolicy):
        out = attribute_policy.redact_attributes(
            {"gen_ai.request.model": "mistral-large"}
        )
        assert out["gen_ai.request.model"] == "mistral-large"

    def test_usage_prefix_kept(self, attribute_policy: AttributeRedactionPolicy):
        out = attribute_policy.redact_attributes({"gen_ai.usage.input_tokens": 42})
        assert out["gen_ai.usage.input_tokens"] == 42

    def test_fragment_match_redacted(self, attribute_policy: AttributeRedactionPolicy):
        out = attribute_policy.redact_attributes(
            {"custom.prompt.text": "secret prompt"}
        )
        assert out["custom.prompt.text"] == DEFAULT_REDACTED_VALUE

    def test_token_pattern_on_kept_string(
        self, attribute_policy: AttributeRedactionPolicy
    ):
        out = attribute_policy.redact_attributes(
            {"note": "call token ghp_abcdefghijklmnopqrstuvwxyz0123 now"}
        )
        assert out["note"] == "call token [REDACTED] now"

    def test_non_primitive_redacted(self, attribute_policy: AttributeRedactionPolicy):
        out = attribute_policy.redact_attributes({"data": ("a", "b")})
        assert out["data"] == DEFAULT_REDACTED_VALUE

    def test_non_primitive_kept_when_disabled(self):
        policy = AttributeRedactionPolicy(redact_non_primitive=False)
        out = policy.redact_attributes({"safeish.list": ("a", "b")})
        assert out["safeish.list"] == ("a", "b")

    def test_string_sequence_scanned_element_wise_when_kept(self):
        policy = AttributeRedactionPolicy(redact_non_primitive=False)
        out = policy.redact_attributes(
            {"tags": ["plain", "ghp_abcdefghijklmnopqrstuvwxyz0123"]}
        )
        assert out["tags"] == ["plain", DEFAULT_REDACTED_VALUE]

    def test_safe_key_string_sequence_scanned(
        self, attribute_policy: AttributeRedactionPolicy
    ):
        out = attribute_policy.redact_attributes(
            {"gen_ai.response.finish_reasons": ("stop", "Bearer abc.def")}
        )
        assert out["gen_ai.response.finish_reasons"] == ("stop", DEFAULT_REDACTED_VALUE)

    def test_none_attributes_returns_empty(
        self, attribute_policy: AttributeRedactionPolicy
    ):
        assert attribute_policy.redact_attributes(None) == {}

    def test_status_description_redacted(
        self, attribute_policy: AttributeRedactionPolicy
    ):
        assert (
            attribute_policy.redact_status_description("boom: user@x.com")
            == DEFAULT_REDACTED_VALUE
        )
        assert attribute_policy.redact_status_description(None) is None

    def test_span_name_unchanged(self, attribute_policy: AttributeRedactionPolicy):
        assert (
            attribute_policy.redact_span_name("chat mistral-large")
            == "chat mistral-large"
        )

    def test_custom_redacted_value(self):
        policy = AttributeRedactionPolicy(redacted_value="XXX")
        out = policy.redact_attributes({"http.url": "https://x"})
        assert out["http.url"] == "XXX"


class TestAttributeRedactionMetadata:
    def test_no_metadata_by_default(
        self, attribute_policy: AttributeRedactionPolicy
    ):
        out = attribute_policy.redact_attributes({"gen_ai.input.messages": "hello"})
        assert out == {"gen_ai.input.messages": DEFAULT_REDACTED_VALUE}

    def test_string_redaction_emits_length(self):
        policy = AttributeRedactionPolicy(emit_redaction_metadata=True)
        out = policy.redact_attributes({"gen_ai.input.messages": "hello"})
        assert out["gen_ai.input.messages"] == DEFAULT_REDACTED_VALUE
        assert out["gen_ai.input.messages.redacted_length"] == 5

    def test_mapping_redaction_emits_count(self):
        policy = AttributeRedactionPolicy(emit_redaction_metadata=True)
        out = policy.redact_attributes(
            cast(dict[str, AttributeValue], {"data": {"a": 1, "b": 2}})
        )
        assert out["data"] == DEFAULT_REDACTED_VALUE
        assert out["data.redacted_count"] == 2

    def test_sequence_redaction_emits_count(self):
        policy = AttributeRedactionPolicy(emit_redaction_metadata=True)
        out = policy.redact_attributes({"data": ("a", "b", "c")})
        assert out["data"] == DEFAULT_REDACTED_VALUE
        assert out["data.redacted_count"] == 3

    def test_other_type_emits_type_name(self):
        policy = AttributeRedactionPolicy(emit_redaction_metadata=True)
        out = policy.redact_attributes(
            cast(dict[str, AttributeValue], {"obj": {1, 2}})
        )
        assert out["obj"] == DEFAULT_REDACTED_VALUE
        assert out["obj.redacted_type"] == "set"

    def test_kept_string_emits_match_count(self):
        policy = AttributeRedactionPolicy(emit_redaction_metadata=True)
        out = policy.redact_attributes(
            {"note": "token ghp_abcdefghijklmnopqrstuvwxyz0123 now"}
        )
        assert out["note"] == "token [REDACTED] now"
        assert out["note.redacted_matches"] == 1

    def test_kept_sequence_sums_match_count(self):
        policy = AttributeRedactionPolicy(
            emit_redaction_metadata=True, redact_non_primitive=False
        )
        out = policy.redact_attributes(
            {"tags": ["plain", "ghp_abcdefghijklmnopqrstuvwxyz0123", "Bearer abc.def"]}
        )
        assert out["tags"] == ["plain", DEFAULT_REDACTED_VALUE, DEFAULT_REDACTED_VALUE]
        assert out["tags.redacted_matches"] == 2

    def test_kept_string_without_match_has_no_metadata(self):
        policy = AttributeRedactionPolicy(emit_redaction_metadata=True)
        out = policy.redact_attributes({"gen_ai.request.model": "mistral-large"})
        assert out == {"gen_ai.request.model": "mistral-large"}

    def test_idempotent_on_already_redacted_attributes(self):
        policy = AttributeRedactionPolicy(emit_redaction_metadata=True)
        first = policy.redact_attributes({"gen_ai.input.messages": "hello"})
        second = policy.redact_attributes(first)
        assert second == first

    def test_idempotent_on_kept_match_metadata(self):
        policy = AttributeRedactionPolicy(emit_redaction_metadata=True)
        first = policy.redact_attributes(
            {"note": "token ghp_abcdefghijklmnopqrstuvwxyz0123 now"}
        )
        second = policy.redact_attributes(first)
        assert second == first


class TestRegexRedactionPolicy:
    def test_email_redacted_inline_preserving_structure(
        self, regex_policy: RegexRedactionPolicy
    ):
        out = regex_policy.redact_attributes(
            {"gen_ai.input.messages": '{"content":"reach me at a@b.com"}'}
        )
        assert out["gen_ai.input.messages"] == '{"content":"reach me at [REDACTED]"}'

    def test_token_redacted(self, regex_policy: RegexRedactionPolicy):
        out = regex_policy.redact_attributes({"h": "Bearer abc.def-ghi"})
        assert out["h"] == "[REDACTED]"

    def test_non_matching_string_kept(self, regex_policy: RegexRedactionPolicy):
        out = regex_policy.redact_attributes({"server.address": "prod-host-1"})
        assert out["server.address"] == "prod-host-1"

    def test_non_string_untouched(self, regex_policy: RegexRedactionPolicy):
        out = regex_policy.redact_attributes({"n": 5, "b": True})
        assert out == {"n": 5, "b": True}

    def test_span_name_scanned(self, regex_policy: RegexRedactionPolicy):
        assert regex_policy.redact_span_name("op a@b.com") == "op [REDACTED]"

    def test_status_description_scanned(self, regex_policy: RegexRedactionPolicy):
        assert (
            regex_policy.redact_status_description("failed for a@b.com")
            == "failed for [REDACTED]"
        )

    @pytest.mark.parametrize(
        "secret",
        [
            "AKIAIOSFODNN7EXAMPLE",
            "AIzaabcdefghijklmnopqrstuvwxyz012345678",
            "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abc123",
            "-----BEGIN RSA PRIVATE KEY-----",
            "sk_live_0123456789abcdefghij",
            "sk-ant-api03-abcdefghijklmnopqrstuvwxyz012345",
            "hf_abcdefghijklmnopqrstuvwxyz0123456789",
            "github_pat_abcdefghijklmnopqrstuvwxyz",
            "glpat-abcdefghij0123456789ab",
            "shpat_0123456789abcdef0123456789abcdef",
            "sq0atp-0123456789abcdefghijkl",
            "PMAK-0123456789abcdefghijklmn",
            "phc_abcdefghijklmnopqrstuvwxyz0123456789abcdefg",
            "SG.abcdefghijklmnopqrstuv.abcdefghijklmnopqrstuvwxyz0123456789abcdefg",
            "pk_live_0123456789abcdefghijklmn",
            "https://hooks.slack.com/services/T00000000/B00000000/abcdefghijklmnopqrstuvwx",
        ],
    )
    def test_secret_patterns_redacted(
        self, regex_policy: RegexRedactionPolicy, secret: str
    ):
        out = regex_policy.redact_attributes({"v": f"leak {secret} here"})
        value = out["v"]
        assert isinstance(value, str)
        assert secret not in value
        assert DEFAULT_REDACTED_VALUE in value

    def test_string_sequence_scanned_preserving_container(
        self, regex_policy: RegexRedactionPolicy
    ):
        out = regex_policy.redact_attributes({"msgs": ["hello", "reach me at a@b.com"]})
        assert out["msgs"] == ["hello", "reach me at [REDACTED]"]

    def test_tuple_sequence_stays_tuple(self, regex_policy: RegexRedactionPolicy):
        out = regex_policy.redact_attributes({"msgs": ("hi", "a@b.com")})
        assert out["msgs"] == ("hi", "[REDACTED]")

    def test_numeric_sequence_untouched(self, regex_policy: RegexRedactionPolicy):
        out = regex_policy.redact_attributes({"nums": [1, 2, 3]})
        assert out["nums"] == [1, 2, 3]


class TestCallbackRedactionPolicy:
    def test_mask_applied_per_attribute(self):
        policy = CallbackRedactionPolicy(
            lambda key, value: "[X]" if "message" in key else value
        )
        out = policy.redact_attributes(
            {"gen_ai.output.messages": "hi", "gen_ai.request.model": "m"}
        )
        assert out == {"gen_ai.output.messages": "[X]", "gen_ai.request.model": "m"}

    def test_returning_none_drops_attribute(self):
        policy = CallbackRedactionPolicy(
            lambda key, value: None if key == "drop" else value
        )
        out = policy.redact_attributes({"drop": "x", "keep": "y"})
        assert out == {"keep": "y"}
