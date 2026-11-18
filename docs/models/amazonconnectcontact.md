# AmazonConnectContact

Contact metadata recorded when Amazon Connect starts a session.


## Fields

| Field                              | Type                               | Required                           | Description                        |
| ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- |
| `type`                             | *Literal["amazon_connect"]*        | :heavy_check_mark:                 | N/A                                |
| `context_id`                       | *str*                              | :heavy_check_mark:                 | Amazon Connect session context ID. |
| `instance_arn`                     | *OptionalNullable[str]*            | :heavy_minus_sign:                 | N/A                                |
| `instance_id`                      | *OptionalNullable[str]*            | :heavy_minus_sign:                 | N/A                                |
| `contact_arn`                      | *OptionalNullable[str]*            | :heavy_minus_sign:                 | N/A                                |
| `contact_id`                       | *OptionalNullable[str]*            | :heavy_minus_sign:                 | N/A                                |
| `caller_number`                    | *OptionalNullable[str]*            | :heavy_minus_sign:                 | N/A                                |
| `called_number`                    | *OptionalNullable[str]*            | :heavy_minus_sign:                 | N/A                                |
| `channel`                          | *OptionalNullable[str]*            | :heavy_minus_sign:                 | N/A                                |