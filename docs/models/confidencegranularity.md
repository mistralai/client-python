# ConfidenceGranularity

Granularity level for OCR confidence scores.

Public API: 'word' and 'page' only.
Internal: 'token' is available for internal tooling (zephyr) but not exposed in the OpenAPI spec.

Note: This schema is hardcoded for removal in open_api.py::_remove_internal_fields
because StrEnum can't carry model_config with x-mistral-visibility.


## Values

| Name    | Value   |
| ------- | ------- |
| `TOKEN` | token   |
| `WORD`  | word    |
| `PAGE`  | page    |