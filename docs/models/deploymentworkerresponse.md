# DeploymentWorkerResponse


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `name`                                                               | *str*                                                                | :heavy_check_mark:                                                   | Worker name                                                          |
| `created_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | When the worker first registered                                     |
| `updated_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | When the worker last registered                                      |
| `is_active`                                                          | *bool*                                                               | :heavy_check_mark:                                                   | Whether this worker's liveness key is currently alive                |