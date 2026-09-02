# Beta.Observability.Traces

## Overview

### Available Operations

* [create_pipeline_config_v1_observability_pipeline_configs_post](#create_pipeline_config_v1_observability_pipeline_configs_post) - Create a worker pipeline configuration
* [list_pipeline_configs_v1_observability_pipeline_configs_get](#list_pipeline_configs_v1_observability_pipeline_configs_get) - List worker pipeline configurations
* [get_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_get](#get_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_get) - Get a worker pipeline configuration
* [update_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_put](#update_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_put) - Replace a worker pipeline configuration
* [delete_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_delete](#delete_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_delete) - Delete a worker pipeline configuration
* [search](#search) - Search traces
* [aggregate](#aggregate) - Aggregate traces
* [get_trace_fields](#get_trace_fields) - Get trace field definitions
* [get_trace_by_id](#get_trace_by_id) - Get trace by id
* [get_trace_spans](#get_trace_spans) - Get trace spans
* [fetch_options](#fetch_options) - Get options for a trace field
* [get_span_by_id](#get_span_by_id) - Get span by id

## create_pipeline_config_v1_observability_pipeline_configs_post

Create a worker pipeline configuration

### Example Usage

<!-- UsageSnippet language="python" operationID="create_pipeline_config_v1_observability_pipeline_configs_post" method="post" path="/v1/observability/pipeline-configs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.create_pipeline_config_v1_observability_pipeline_configs_post(pipeline_kind="judge", selectors=[], definition={
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

## list_pipeline_configs_v1_observability_pipeline_configs_get

List worker pipeline configurations

### Example Usage

<!-- UsageSnippet language="python" operationID="list_pipeline_configs_v1_observability_pipeline_configs_get" method="get" path="/v1/observability/pipeline-configs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.list_pipeline_configs_v1_observability_pipeline_configs_get()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                             | Type                                                                  | Required                                                              | Description                                                           |
| --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `pipeline_kind`                                                       | [OptionalNullable[models.PipelineKind]](../../models/pipelinekind.md) | :heavy_minus_sign:                                                    | N/A                                                                   |
| `group`                                                               | *OptionalNullable[str]*                                               | :heavy_minus_sign:                                                    | N/A                                                                   |
| `enabled`                                                             | *OptionalNullable[bool]*                                              | :heavy_minus_sign:                                                    | N/A                                                                   |
| `retries`                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)      | :heavy_minus_sign:                                                    | Configuration to override the default retry behavior of the client.   |

### Response

**[models.PipelineConfigsResponse](../../models/pipelineconfigsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_get

Get a worker pipeline configuration

### Example Usage

<!-- UsageSnippet language="python" operationID="get_pipeline_config_v1_observability_pipeline_configs__pipeline_config_id__get" method="get" path="/v1/observability/pipeline-configs/{pipeline_config_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.get_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_get(pipeline_config_id="939fdf7d-2edf-45ca-bb75-a47326da1799")

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

## update_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_put

Replace a worker pipeline configuration

### Example Usage

<!-- UsageSnippet language="python" operationID="update_pipeline_config_v1_observability_pipeline_configs__pipeline_config_id__put" method="put" path="/v1/observability/pipeline-configs/{pipeline_config_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.update_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_put(pipeline_config_id="4ee75abd-cccd-4232-9858-0c535465bfd5", pipeline_kind="detection", selectors=[], definition={
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

## delete_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_delete

Delete a worker pipeline configuration

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_pipeline_config_v1_observability_pipeline_configs__pipeline_config_id__delete" method="delete" path="/v1/observability/pipeline-configs/{pipeline_config_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.traces.delete_pipeline_config_v1_observability_pipeline_configs_pipeline_config_id_delete(pipeline_config_id="816cdd49-f7b2-4941-a73d-af3c25958c4d")

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

## search

Search traces

### Example Usage

<!-- UsageSnippet language="python" operationID="search_traces_v1_observability_traces_search_post" method="post" path="/v1/observability/traces/search" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.search(page_size=50)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `from_`                                                              | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `to`                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `page_size`                                                          | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `cursor`                                                             | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `search_expression`                                                  | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |

### Response

**[models.GetTraces](../../models/gettraces.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## aggregate

Aggregate traces

### Example Usage

<!-- UsageSnippet language="python" operationID="aggregate_traces_v1_observability_traces_aggregate_post" method="post" path="/v1/observability/traces/aggregate" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.aggregate(metric={
        "measure": "<value>",
        "aggregation": "p95",
    }, limit=1000)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                               | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `metric`                                                                | [models.MetricDefinition](../../models/metricdefinition.md)             | :heavy_check_mark:                                                      | N/A                                                                     |
| `from_`                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects)    | :heavy_minus_sign:                                                      | N/A                                                                     |
| `to`                                                                    | [date](https://docs.python.org/3/library/datetime.html#date-objects)    | :heavy_minus_sign:                                                      | N/A                                                                     |
| `dimensions`                                                            | List[*str*]                                                             | :heavy_minus_sign:                                                      | N/A                                                                     |
| `time_dimension`                                                        | [OptionalNullable[models.TimeDimension]](../../models/timedimension.md) | :heavy_minus_sign:                                                      | N/A                                                                     |
| `search_expression`                                                     | *OptionalNullable[str]*                                                 | :heavy_minus_sign:                                                      | N/A                                                                     |
| `order_by`                                                              | List[[models.OrderByClause](../../models/orderbyclause.md)]             | :heavy_minus_sign:                                                      | N/A                                                                     |
| `limit`                                                                 | *Optional[int]*                                                         | :heavy_minus_sign:                                                      | N/A                                                                     |
| `retries`                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)        | :heavy_minus_sign:                                                      | Configuration to override the default retry behavior of the client.     |

### Response

**[models.Aggregation](../../models/aggregation.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get_trace_fields

Get trace field definitions

### Example Usage

<!-- UsageSnippet language="python" operationID="get_trace_fields_v1_observability_traces_fields_get" method="get" path="/v1/observability/traces/fields" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.get_trace_fields()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetTraceFields](../../models/gettracefields.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get_trace_by_id

Get trace by id

### Example Usage

<!-- UsageSnippet language="python" operationID="get_trace_by_id_v1_observability_traces__trace_id__get" method="get" path="/v1/observability/traces/{trace_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.get_trace_by_id(trace_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `trace_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetTrace](../../models/gettrace.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get_trace_spans

Get trace spans

### Example Usage

<!-- UsageSnippet language="python" operationID="get_trace_spans_v1_observability_traces__trace_id__spans_get" method="get" path="/v1/observability/traces/{trace_id}/spans" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.get_trace_spans(trace_id="<id>", page_size=50)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `trace_id`                                                           | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `from_`                                                              | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `to`                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `page_size`                                                          | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `cursor`                                                             | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |

### Response

**[models.GetSpans](../../models/getspans.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch_options

Get options for a trace field

### Example Usage

<!-- UsageSnippet language="python" operationID="get_trace_field_options_v1_observability_traces_fields__field_name__options_get" method="get" path="/v1/observability/traces/fields/{field_name}/options" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.fetch_options(field_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `field_name`                                                         | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `from_`                                                              | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `to`                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |

### Response

**[models.GetTraceFieldOptions](../../models/gettracefieldoptions.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get_span_by_id

Get span by id

### Example Usage

<!-- UsageSnippet language="python" operationID="get_span_by_id_v1_observability_traces__trace_id__spans__span_id__get" method="get" path="/v1/observability/traces/{trace_id}/spans/{span_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.traces.get_span_by_id(trace_id="<id>", span_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `trace_id`                                                           | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `span_id`                                                            | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `from_`                                                              | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `to`                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |

### Response

**[models.GetSpan](../../models/getspan.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |