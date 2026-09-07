# Beta.Observability.Evaluations

## Overview

### Available Operations

* [create_pipeline_config](#create_pipeline_config) - Create a worker pipeline configuration
* [list_pipeline_configs](#list_pipeline_configs) - List worker pipeline configurations
* [get_pipeline_config](#get_pipeline_config) - Get a worker pipeline configuration
* [update_pipeline_config](#update_pipeline_config) - Replace a worker pipeline configuration
* [delete_pipeline_config](#delete_pipeline_config) - Delete a worker pipeline configuration

## create_pipeline_config

Create a worker pipeline configuration

### Example Usage

<!-- UsageSnippet language="python" operationID="create_pipeline_config_v1_observability_pipeline_configs_post" method="post" path="/v1/observability/pipeline-configs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.create_pipeline_config(pipeline_kind="judge", selectors=[], definition={
        "model": "Golf",
        "prompt": "<value>",
    }, name="<value>", enabled=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `pipeline_kind`                                                               | [models.PipelineKind](../../models/pipelinekind.md)                           | :heavy_check_mark:                                                            | N/A                                                                           |
| `selectors`                                                                   | List[[models.PipelineConfigSelector](../../models/pipelineconfigselector.md)] | :heavy_check_mark:                                                            | N/A                                                                           |
| `definition`                                                                  | [models.PipelineConfigDefinition](../../models/pipelineconfigdefinition.md)   | :heavy_check_mark:                                                            | N/A                                                                           |
| `name`                                                                        | *str*                                                                         | :heavy_check_mark:                                                            | N/A                                                                           |
| `description`                                                                 | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `slug`                                                                        | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `group`                                                                       | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `enabled`                                                                     | *Optional[bool]*                                                              | :heavy_minus_sign:                                                            | N/A                                                                           |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |

### Response

**[models.PipelineConfig](../../models/pipelineconfig.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## list_pipeline_configs

List worker pipeline configurations

### Example Usage

<!-- UsageSnippet language="python" operationID="list_pipeline_configs_v1_observability_pipeline_configs_get" method="get" path="/v1/observability/pipeline-configs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.list_pipeline_configs(page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                             | Type                                                                  | Required                                                              | Description                                                           |
| --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `pipeline_kind`                                                       | [OptionalNullable[models.PipelineKind]](../../models/pipelinekind.md) | :heavy_minus_sign:                                                    | N/A                                                                   |
| `group`                                                               | *OptionalNullable[str]*                                               | :heavy_minus_sign:                                                    | N/A                                                                   |
| `enabled`                                                             | *OptionalNullable[bool]*                                              | :heavy_minus_sign:                                                    | N/A                                                                   |
| `page_size`                                                           | *Optional[int]*                                                       | :heavy_minus_sign:                                                    | N/A                                                                   |
| `page`                                                                | *Optional[int]*                                                       | :heavy_minus_sign:                                                    | N/A                                                                   |
| `q`                                                                   | *OptionalNullable[str]*                                               | :heavy_minus_sign:                                                    | N/A                                                                   |
| `retries`                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)      | :heavy_minus_sign:                                                    | Configuration to override the default retry behavior of the client.   |

### Response

**[models.PipelineConfigsResponse](../../models/pipelineconfigsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get_pipeline_config

Get a worker pipeline configuration

### Example Usage

<!-- UsageSnippet language="python" operationID="get_pipeline_config_v1_observability_pipeline_configs__pipeline_config_id__get" method="get" path="/v1/observability/pipeline-configs/{pipeline_config_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.get_pipeline_config(pipeline_config_id="939fdf7d-2edf-45ca-bb75-a47326da1799")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `pipeline_config_id`                                                | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PipelineConfig](../../models/pipelineconfig.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## update_pipeline_config

Replace a worker pipeline configuration

### Example Usage

<!-- UsageSnippet language="python" operationID="update_pipeline_config_v1_observability_pipeline_configs__pipeline_config_id__put" method="put" path="/v1/observability/pipeline-configs/{pipeline_config_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.update_pipeline_config(pipeline_config_id="4ee75abd-cccd-4232-9858-0c535465bfd5", pipeline_kind="detection", selectors=[], definition={
        "destination": {
            "protocol": "<value>",
            "endpoint": "<value>",
            "insecure": False,
        },
    }, name="<value>", enabled=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `pipeline_config_id`                                                          | *str*                                                                         | :heavy_check_mark:                                                            | N/A                                                                           |
| `pipeline_kind`                                                               | [models.PipelineKind](../../models/pipelinekind.md)                           | :heavy_check_mark:                                                            | N/A                                                                           |
| `selectors`                                                                   | List[[models.PipelineConfigSelector](../../models/pipelineconfigselector.md)] | :heavy_check_mark:                                                            | N/A                                                                           |
| `definition`                                                                  | [models.PipelineConfigDefinition](../../models/pipelineconfigdefinition.md)   | :heavy_check_mark:                                                            | N/A                                                                           |
| `name`                                                                        | *str*                                                                         | :heavy_check_mark:                                                            | N/A                                                                           |
| `enabled`                                                                     | *bool*                                                                        | :heavy_check_mark:                                                            | N/A                                                                           |
| `description`                                                                 | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `slug`                                                                        | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `group`                                                                       | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |

### Response

**[models.PipelineConfig](../../models/pipelineconfig.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## delete_pipeline_config

Delete a worker pipeline configuration

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_pipeline_config_v1_observability_pipeline_configs__pipeline_config_id__delete" method="delete" path="/v1/observability/pipeline-configs/{pipeline_config_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.evaluations.delete_pipeline_config(pipeline_config_id="816cdd49-f7b2-4941-a73d-af3c25958c4d")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `pipeline_config_id`                                                | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |