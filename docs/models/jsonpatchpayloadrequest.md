# JSONPatchPayloadRequest

A payload containing a list of JSON Patch operations.

Used for streaming incremental updates to workflow state.


## Fields

| Field                                                                                  | Type                                                                                   | Required                                                                               | Description                                                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `type`                                                                                 | *Literal["json_patch"]*                                                                | :heavy_check_mark:                                                                     | Discriminator indicating this is a JSON Patch payload.                                 |
| `value`                                                                                | List[[models.JSONPatchPayloadRequestValue](../models/jsonpatchpayloadrequestvalue.md)] | :heavy_check_mark:                                                                     | The list of JSON Patch operations to apply in order.                                   |