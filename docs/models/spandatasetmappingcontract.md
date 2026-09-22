# SpanDatasetMappingContract

Mapping rules applied independently to every requested telemetry span.

Version 1 mappings are optional per span: a missing, null, blank-string, or empty-array
source omits the target key. JSON object and array strings become structured values;
scalar-looking and malformed JSON strings remain strings.


## Fields

| Field                                                              | Type                                                               | Required                                                           | Description                                                        |
| ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `version`                                                          | *Literal[1]*                                                       | :heavy_check_mark:                                                 | N/A                                                                |
| `mappings`                                                         | List[[models.SpanDatasetMapping](../models/spandatasetmapping.md)] | :heavy_check_mark:                                                 | N/A                                                                |