# CompletionTokensDetails

Token usage details for the completion.

``reasoning_tokens`` is ``None`` when the provider did not report a count.
Preserve that distinction instead of inventing a measured zero: ``0`` means
"reasoning off, confirmed by the provider", ``None`` means "unknown".


## Fields

| Field                   | Type                    | Required                | Description             |
| ----------------------- | ----------------------- | ----------------------- | ----------------------- |
| `reasoning_tokens`      | *OptionalNullable[int]* | :heavy_minus_sign:      | N/A                     |