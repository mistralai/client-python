# JSONPatchPayloadResponse

A payload containing a list of JSON Patch operations.

Used for streaming incremental updates to workflow state.
When encrypted, the value field contains base64-encoded encrypted data
and encoding_options indicates the type of encryption applied.


## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `type`                                                                   | *Literal["json_patch"]*                                                  | :heavy_check_mark:                                                       | Discriminator indicating this is a JSON Patch payload.                   |
| `value`                                                                  | [models.JSONPatchPayloadValue](../models/jsonpatchpayloadvalue.md)       | :heavy_check_mark:                                                       | N/A                                                                      |
| `encoding_options`                                                       | List[[models.EncodedPayloadOptions](../models/encodedpayloadoptions.md)] | :heavy_check_mark:                                                       | Encoding options applied to the payload.                                 |