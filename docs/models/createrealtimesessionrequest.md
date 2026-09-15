# CreateRealtimeSessionRequest

Payload used to create realtime client sessions.


## Fields

| Field                   | Type                    | Required                | Description             |
| ----------------------- | ----------------------- | ----------------------- | ----------------------- |
| `purpose`               | *Literal["realtime"]*   | :heavy_check_mark:      | N/A                     |
| `model`                 | *str*                   | :heavy_check_mark:      | N/A                     |
| `ttl_seconds`           | *OptionalNullable[int]* | :heavy_minus_sign:      | N/A                     |