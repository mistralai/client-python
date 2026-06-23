# ConnectError

Error response.


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              | Example                                                  |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `code`                                                   | [Optional[models.Code]](../models/code.md)               | :heavy_minus_sign:                                       | Machine-readable error code.                             | not_found                                                |
| `message`                                                | *Optional[str]*                                          | :heavy_minus_sign:                                       | Human-readable error message.                            |                                                          |
| `detail`                                                 | [Optional[models.ProtobufAny]](../models/protobufany.md) | :heavy_minus_sign:                                       | Additional structured error detail.                      |                                                          |
| `__pydantic_extra__`                                     | Dict[str, *Any*]                                         | :heavy_minus_sign:                                       | N/A                                                      |                                                          |