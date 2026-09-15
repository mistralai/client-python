# SearchLogsV1ObservabilityLogsSearchPostRequest


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `from_`                                                              | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `to`                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `page_size`                                                          | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `cursor`                                                             | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `logs_request`                                                       | [models.LogsRequest](../models/logsrequest.md)                       | :heavy_check_mark:                                                   | N/A                                                                  |