# Beta.Rag.IngestionPipelineConfigurations

## Overview

### Available Operations

* [list](#list) - List ingestion pipeline configurations
* [register](#register) - Register Config
* [update_run_info](#update_run_info) - Update Run Info

## list

For the current workspace, lists all of the registered ingestion pipeline configurations.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_configs_v1_rag_ingestion_pipeline_configurations_get" method="get" path="/v1/rag/ingestion_pipeline_configurations" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.ingestion_pipeline_configurations.list()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.IngestionPipelineConfiguration]](../../models/.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## register

Register an ingestion configuration.

### Example Usage

<!-- UsageSnippet language="python" operationID="register_config_v1_rag_ingestion_pipeline_configurations_put" method="put" path="/v1/rag/ingestion_pipeline_configurations" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.ingestion_pipeline_configurations.register(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `pipeline_composition`                                              | Dict[str, *str*]                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.IngestionPipelineConfiguration](../../models/ingestionpipelineconfiguration.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_run_info

Update Run Info

### Example Usage

<!-- UsageSnippet language="python" operationID="update_run_info_v1_rag_ingestion_pipeline_configurations__id__run_info_put" method="put" path="/v1/rag/ingestion_pipeline_configurations/{id}/run_info" -->
```python
from mistralai.client import Mistral
from mistralai.client.utils import parse_datetime
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.ingestion_pipeline_configurations.update_run_info(id="6b630c1b-b57e-4237-a015-ff6247cbbcf8", execution_time=parse_datetime("2024-06-27T06:29:04.390Z"), chunks_count=983906)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `id`                                                                 | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `execution_time`                                                     | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | N/A                                                                  |
| `chunks_count`                                                       | *int*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |

### Response

**[models.IngestionPipelineConfiguration](../../models/ingestionpipelineconfiguration.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |