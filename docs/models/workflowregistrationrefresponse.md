# WorkflowRegistrationRefResponse


## Fields

| Field                                    | Type                                     | Required                                 | Description                              |
| ---------------------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| `workflow_id`                            | *str*                                    | :heavy_check_mark:                       | The workflow ID                          |
| `workflow_registration_id`               | *OptionalNullable[str]*                  | :heavy_minus_sign:                       | The workflow registration ID             |
| `workflow_version_id`                    | *str*                                    | :heavy_check_mark:                       | Deprecated: use workflow_registration_id |