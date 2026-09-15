# ExecutionLogRecord


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `timestamp`                                                          | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | N/A                                                                  |
| `trace_id`                                                           | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `span_id`                                                            | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `severity_text`                                                      | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `body`                                                               | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `log_attributes`                                                     | Dict[str, *str*]                                                     | :heavy_check_mark:                                                   | N/A                                                                  |