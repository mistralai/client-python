# PublicExecutionEnv

Credentials-free projection of ExecutionEnv for the public /connectors/mistral response.


## Fields

| Field                                                                            | Type                                                                             | Required                                                                         | Description                                                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `tools`                                                                          | List[[models.Tool](../models/tool.md)]                                           | :heavy_check_mark:                                                               | N/A                                                                              |
| `public_connector_execution_data`                                                | [models.PublicConnectorExecutionData](../models/publicconnectorexecutiondata.md) | :heavy_check_mark:                                                               | N/A                                                                              |
| `errors`                                                                         | List[*str*]                                                                      | :heavy_check_mark:                                                               | N/A                                                                              |