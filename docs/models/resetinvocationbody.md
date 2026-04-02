# ResetInvocationBody


## Fields

| Field                                                          | Type                                                           | Required                                                       | Description                                                    |
| -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| `event_id`                                                     | *int*                                                          | :heavy_check_mark:                                             | The event ID to reset the workflow execution to                |
| `reason`                                                       | *OptionalNullable[str]*                                        | :heavy_minus_sign:                                             | Reason for resetting the workflow execution                    |
| `exclude_signals`                                              | *Optional[bool]*                                               | :heavy_minus_sign:                                             | Whether to exclude signals that happened after the reset point |
| `exclude_updates`                                              | *Optional[bool]*                                               | :heavy_minus_sign:                                             | Whether to exclude updates that happened after the reset point |