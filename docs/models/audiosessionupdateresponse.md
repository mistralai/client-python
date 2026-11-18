# AudioSessionUpdateResponse

The session the update was sent to. The agent applies the update at its
next turn boundary and reports the outcome through the `session_updated`
and `session_update_failed` webhooks.


## Fields

| Field                                                                                    | Type                                                                                     | Required                                                                                 | Description                                                                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `id`                                                                                     | *str*                                                                                    | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `status`                                                                                 | [models.AudioSessionUpdateResponseStatus](../models/audiosessionupdateresponsestatus.md) | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `num_participants`                                                                       | *int*                                                                                    | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `created_at`                                                                             | [date](https://docs.python.org/3/library/datetime.html#date-objects)                     | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `phone_call`                                                                             | [OptionalNullable[models.AudioSessionPhoneCall]](../models/audiosessionphonecall.md)     | :heavy_minus_sign:                                                                       | N/A                                                                                      |
| `bridge_metadata`                                                                        | [OptionalNullable[models.AmazonConnectContact]](../models/amazonconnectcontact.md)       | :heavy_minus_sign:                                                                       | N/A                                                                                      |