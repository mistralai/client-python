# JSONPayloadRequest

A payload containing arbitrary JSON data.

Used for complete state snapshots or final results.


## Fields

| Field                                                | Type                                                 | Required                                             | Description                                          |
| ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| `type`                                               | *Optional[Literal["json"]]*                          | :heavy_minus_sign:                                   | Discriminator indicating this is a raw JSON payload. |
| `value`                                              | *Any*                                                | :heavy_check_mark:                                   | The JSON-serializable payload value.                 |