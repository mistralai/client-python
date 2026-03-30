# DeploymentResponse


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `id`                                                                 | *str*                                                                | :heavy_check_mark:                                                   | Unique identifier of the deployment                                  |
| `name`                                                               | *str*                                                                | :heavy_check_mark:                                                   | Deployment name                                                      |
| `is_active`                                                          | *bool*                                                               | :heavy_check_mark:                                                   | Whether at least one worker is currently live                        |
| `created_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | When the deployment was first registered                             |
| `updated_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | When the deployment was last updated                                 |