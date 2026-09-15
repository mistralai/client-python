# ScheduleRecentExecution


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `scheduled_at`                                                       | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | Time the execution was scheduled to run.                             |
| `started_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | Actual time the execution started.                                   |
| `execution_id`                                                       | *str*                                                                | :heavy_check_mark:                                                   | ID of the workflow execution that was started.                       |