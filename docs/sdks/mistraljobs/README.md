# Batch.Jobs

## Overview

### Available Operations

* [list](#list) - Get Batch Jobs
* [create](#create) - Create Batch Job
* [get](#get) - Get Batch Job
* [cancel](#cancel) - Cancel Batch Job

## list

Get a list of batch jobs for your organization and user.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_batch_get_batch_jobs" method="get" path="/v1/batch/jobs" -->
```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.batch.jobs.list(page=0, page_size=100, created_by_me=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `page`                                                               | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `page_size`                                                          | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `model`                                                              | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `agent_id`                                                           | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `metadata`                                                           | Dict[str, *Any*]                                                     | :heavy_minus_sign:                                                   | N/A                                                                  |
| `created_after`                                                      | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `created_by_me`                                                      | *Optional[bool]*                                                     | :heavy_minus_sign:                                                   | N/A                                                                  |
| `status`                                                             | List[[models.BatchJobStatus](../../models/batchjobstatus.md)]        | :heavy_minus_sign:                                                   | N/A                                                                  |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |

### Response

**[models.BatchJobsOut](../../models/batchjobsout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## create

Create a new batch job, it will be queued for processing.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_batch_create_batch_job" method="post" path="/v1/batch/jobs" -->
```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.batch.jobs.create(input_files=[
        "fe3343a2-3b8d-404b-ba32-a78dede2614a",
    ], endpoint="/v1/moderations", model="mistral-small-latest", timeout_hours=24)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Example                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `input_files`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | List[*str*]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | The list of input files to be used for batch inference, these files should be `jsonl` files, containing the input data corresponding to the bory request for the batch inference in a "body" field. An example of such file is the following: ```json {"custom_id": "0", "body": {"max_tokens": 100, "messages": [{"role": "user", "content": "What is the best French cheese?"}]}} {"custom_id": "1", "body": {"max_tokens": 100, "messages": [{"role": "user", "content": "What is the best French wine?"}]}} ``` |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `endpoint`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | [models.APIEndpoint](../../models/apiendpoint.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `model`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | The model to be used for batch inference.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | mistral-small-latest                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `agent_id`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | In case you want to use a specific agent from the **deprecated** agents api for batch inference, you can specify the agent ID here.                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `metadata`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Dict[str, *str*]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | The metadata of your choice to be associated with the batch inference job.                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `timeout_hours`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | *Optional[int]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | The timeout in hours for the batch inference job.                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `retries`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

### Response

**[models.BatchJobOut](../../models/batchjobout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## get

Get a batch job details by its UUID.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_batch_get_batch_job" method="get" path="/v1/batch/jobs/{job_id}" -->
```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.batch.jobs.get(job_id="4017dc9f-b629-42f4-9700-8c681b9e7f0f")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `job_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.BatchJobOut](../../models/batchjobout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## cancel

Request the cancellation of a batch job.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_batch_cancel_batch_job" method="post" path="/v1/batch/jobs/{job_id}/cancel" -->
```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.batch.jobs.cancel(job_id="4fb29d1c-535b-4f0a-a1cb-2167f86da569")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `job_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.BatchJobOut](../../models/batchjobout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |