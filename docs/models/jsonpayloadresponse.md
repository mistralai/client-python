# JSONPayloadResponse

A payload containing arbitrary JSON data.

Used for complete state snapshots or final results.
When encrypted, the value field contains base64-encoded encrypted data
and encoding_options indicates the type of encryption applied.


## Fields

| Field                                                                              | Type                                                                               | Required                                                                           | Description                                                                        |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `type`                                                                             | *Optional[Literal["json"]]*                                                        | :heavy_minus_sign:                                                                 | Discriminator indicating this is a raw JSON payload.                               |
| `value`                                                                            | *Any*                                                                              | :heavy_check_mark:                                                                 | The JSON-serializable payload value. When encrypted, contains base64-encoded data. |
| `encoding_options`                                                                 | List[[models.EncodedPayloadOptions](../models/encodedpayloadoptions.md)]           | :heavy_minus_sign:                                                                 | Encoding options applied to the payload.                                           |