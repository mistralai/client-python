# CreateRealtimeSessionResponse


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `object`                                                             | *Optional[Literal["client.session"]]*                                | :heavy_minus_sign:                                                   | N/A                                                                  |
| `purpose`                                                            | [models.ClientSessionPurpose](../models/clientsessionpurpose.md)     | :heavy_check_mark:                                                   | Supported purposes for client sessions.                              |
| `expires_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | N/A                                                                  |
| `client_secret`                                                      | [models.ClientSecret](../models/clientsecret.md)                     | :heavy_check_mark:                                                   | N/A                                                                  |