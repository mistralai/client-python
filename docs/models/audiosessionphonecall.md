# AudioSessionPhoneCall

The phone line a session is attached to.

Present only when the caller reached the agent over telephony, `null` for a
session started from a browser or the API.


## Fields

| Field                                                                                      | Type                                                                                       | Required                                                                                   | Description                                                                                |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `phone_number_id`                                                                          | *str*                                                                                      | :heavy_check_mark:                                                                         | N/A                                                                                        |
| `phone_number`                                                                             | [OptionalNullable[models.AudioSessionPhoneNumber]](../models/audiosessionphonenumber.md)   | :heavy_minus_sign:                                                                         | The number as it stands now, or null once it has been released or when you cannot read it. |