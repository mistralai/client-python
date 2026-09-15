# StreamDeploymentLogsResponseBody

Stream of Server-Sent Events (SSE): `log` events carry a DeploymentLogRecord; `error` events carry a StreamError payload.


## Fields

| Field                                                                                | Type                                                                                 | Required                                                                             | Description                                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `event`                                                                              | [Optional[models.StreamDeploymentLogsEvent]](../models/streamdeploymentlogsevent.md) | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `id`                                                                                 | *Optional[str]*                                                                      | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `data`                                                                               | [Optional[models.StreamDeploymentLogsData]](../models/streamdeploymentlogsdata.md)   | :heavy_minus_sign:                                                                   | N/A                                                                                  |