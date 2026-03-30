# NetworkEncodedInput


## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `b64payload`                                                             | *str*                                                                    | :heavy_check_mark:                                                       | The encoded payload                                                      |
| `encoding_options`                                                       | List[[models.EncodedPayloadOptions](../models/encodedpayloadoptions.md)] | :heavy_minus_sign:                                                       | The encoding of the payload                                              |
| `empty`                                                                  | *Optional[bool]*                                                         | :heavy_minus_sign:                                                       | Whether the payload is empty                                             |