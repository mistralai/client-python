# Datacapture.Extract.Jobs

## Overview

### Available Operations

* [list](#list) - Get Datacapture Extract Jobs
* [create](#create) - Create Datacapture Extract Job
* [get](#get) - Get Datacapture Extract Job
* [cancel](#cancel) - Cancel Datacapture Extract Job
* [list_models](#list_models) - Get Available Models

## list

Get a list of datacapture extract jobs for your organization and user.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_datacapture_extract_get_datacapture_extract_jobs" method="get" path="/v1/datacapture_extract/jobs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.datacapture.extract.jobs.list(page=0, page_size=100, created_by_me=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                           | Type                                                                                                | Required                                                                                            | Description                                                                                         |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `page`                                                                                              | *Optional[int]*                                                                                     | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `page_size`                                                                                         | *Optional[int]*                                                                                     | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `model`                                                                                             | *OptionalNullable[str]*                                                                             | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `organization_uuid`                                                                                 | *OptionalNullable[str]*                                                                             | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `metadata`                                                                                          | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `created_after`                                                                                     | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `created_by_me`                                                                                     | *Optional[bool]*                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `status`                                                                                            | [OptionalNullable[models.DataCaptureExtractJobStatus]](../../models/datacaptureextractjobstatus.md) | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `retries`                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                    | :heavy_minus_sign:                                                                                  | Configuration to override the default retry behavior of the client.                                 |

### Response

**[models.DataCaptureExtractJobsOut](../../models/datacaptureextractjobsout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create

Create a new data capture extract job, it will be queued for processing.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_datacapture_extract_create_datacapture_extract_job" method="post" path="/v1/datacapture_extract/jobs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.datacapture.extract.jobs.create(data_source="api", timeout_hours=48)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                     | Type                                                                                                                          | Required                                                                                                                      | Description                                                                                                                   |
| ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `organization_uuid`                                                                                                           | *OptionalNullable[str]*                                                                                                       | :heavy_minus_sign:                                                                                                            | N/A                                                                                                                           |
| `model`                                                                                                                       | *OptionalNullable[str]*                                                                                                       | :heavy_minus_sign:                                                                                                            | N/A                                                                                                                           |
| `start_date`                                                                                                                  | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                                          | :heavy_minus_sign:                                                                                                            | N/A                                                                                                                           |
| `end_date`                                                                                                                    | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                                          | :heavy_minus_sign:                                                                                                            | N/A                                                                                                                           |
| `data_source`                                                                                                                 | [Optional[models.DataCaptureExtractJobInDatacaptureSourceType]](../../models/datacaptureextractjobindatacapturesourcetype.md) | :heavy_minus_sign:                                                                                                            | N/A                                                                                                                           |
| `capture_reasons`                                                                                                             | List[[models.CaptureReason](../../models/capturereason.md)]                                                                   | :heavy_minus_sign:                                                                                                            | N/A                                                                                                                           |
| `metadata`                                                                                                                    | Dict[str, *str*]                                                                                                              | :heavy_minus_sign:                                                                                                            | N/A                                                                                                                           |
| `timeout_hours`                                                                                                               | *Optional[int]*                                                                                                               | :heavy_minus_sign:                                                                                                            | N/A                                                                                                                           |
| `retries`                                                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                              | :heavy_minus_sign:                                                                                                            | Configuration to override the default retry behavior of the client.                                                           |

### Response

**[models.DataCaptureExtractJobOut](../../models/datacaptureextractjobout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get

Get a data capture extract job details by its UUID.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_datacapture_extract_get_datacapture_extract_job" method="get" path="/v1/datacapture_extract/jobs/{job_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.datacapture.extract.jobs.get(job_id="57a0d257-10b6-48a6-8f70-223bc550546e")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `job_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DetailedDataCaptureExtractJobOut](../../models/detaileddatacaptureextractjobout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## cancel

Request the cancellation of a data capture extract job.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_datacapture_extract_cancel_datacapture_extract_job" method="post" path="/v1/datacapture_extract/jobs/{job_id}/cancel" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.datacapture.extract.jobs.cancel(job_id="432e6edb-218a-42b9-b9a6-a38e5b094b10")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `job_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DataCaptureExtractJobOut](../../models/datacaptureextractjobout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## list_models

Get Available Models

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_datacapture_extract_get_available_models" method="get" path="/v1/datacapture_extract/models" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.datacapture.extract.jobs.list_models()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DataCaptureExtractAvailableModels](../../models/datacaptureextractavailablemodels.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |