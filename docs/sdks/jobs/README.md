# FineTuning.Jobs

## Overview

### Available Operations

* [list](#list) - Get Fine Tuning Jobs
* [create](#create) - Create Fine Tuning Job
* [get](#get) - Get Fine Tuning Job
* [cancel](#cancel) - Cancel Fine Tuning Job
* [start](#start) - Start Fine Tuning Job

## list

Get a list of fine-tuning jobs for your organization and user.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_fine_tuning_get_fine_tuning_jobs" method="get" path="/v1/fine_tuning/jobs" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.fine_tuning.jobs.list(page=0, page_size=100, created_by_me=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                          | Type                                                                                               | Required                                                                                           | Description                                                                                        |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `page`                                                                                             | *Optional[int]*                                                                                    | :heavy_minus_sign:                                                                                 | The page number of the results to be returned.                                                     |
| `page_size`                                                                                        | *Optional[int]*                                                                                    | :heavy_minus_sign:                                                                                 | The number of items to return per page.                                                            |
| `model`                                                                                            | *OptionalNullable[str]*                                                                            | :heavy_minus_sign:                                                                                 | The model name used for fine-tuning to filter on. When set, the other results are not displayed.   |
| `created_after`                                                                                    | [date](https://docs.python.org/3/library/datetime.html#date-objects)                               | :heavy_minus_sign:                                                                                 | The date/time to filter on. When set, the results for previous creation times are not displayed.   |
| `created_before`                                                                                   | [date](https://docs.python.org/3/library/datetime.html#date-objects)                               | :heavy_minus_sign:                                                                                 | N/A                                                                                                |
| `created_by_me`                                                                                    | *Optional[bool]*                                                                                   | :heavy_minus_sign:                                                                                 | When set, only return results for jobs created by the API caller. Other results are not displayed. |
| `status`                                                                                           | [OptionalNullable[models.QueryParamStatus]](../../models/queryparamstatus.md)                      | :heavy_minus_sign:                                                                                 | The current job state to filter on. When set, the other results are not displayed.                 |
| `wandb_project`                                                                                    | *OptionalNullable[str]*                                                                            | :heavy_minus_sign:                                                                                 | The Weights and Biases project to filter on. When set, the other results are not displayed.        |
| `wandb_name`                                                                                       | *OptionalNullable[str]*                                                                            | :heavy_minus_sign:                                                                                 | The Weight and Biases run name to filter on. When set, the other results are not displayed.        |
| `suffix`                                                                                           | *OptionalNullable[str]*                                                                            | :heavy_minus_sign:                                                                                 | The model suffix to filter on. When set, the other results are not displayed.                      |
| `retries`                                                                                          | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                   | :heavy_minus_sign:                                                                                 | Configuration to override the default retry behavior of the client.                                |

### Response

**[models.JobsOut](../../models/jobsout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## create

Create a new fine-tuning job, it will be queued for processing.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_fine_tuning_create_fine_tuning_job" method="post" path="/v1/fine_tuning/jobs" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.fine_tuning.jobs.create(model="Camaro", hyperparameters={
        "learning_rate": 0.0001,
    }, invalid_sample_skip_percentage=0)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                                                         | Type                                                                                                                                                                                                                                                                                                                                                              | Required                                                                                                                                                                                                                                                                                                                                                          | Description                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                                                                                                                                                                                                                                                                                                                                                           | *str*                                                                                                                                                                                                                                                                                                                                                             | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                | The name of the model to fine-tune.                                                                                                                                                                                                                                                                                                                               |
| `hyperparameters`                                                                                                                                                                                                                                                                                                                                                 | [models.Hyperparameters](../../models/hyperparameters.md)                                                                                                                                                                                                                                                                                                         | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                | N/A                                                                                                                                                                                                                                                                                                                                                               |
| `training_files`                                                                                                                                                                                                                                                                                                                                                  | List[[models.TrainingFile](../../models/trainingfile.md)]                                                                                                                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | N/A                                                                                                                                                                                                                                                                                                                                                               |
| `validation_files`                                                                                                                                                                                                                                                                                                                                                | List[*str*]                                                                                                                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | A list containing the IDs of uploaded files that contain validation data. If you provide these files, the data is used to generate validation metrics periodically during fine-tuning. These metrics can be viewed in `checkpoints` when getting the status of a running fine-tuning job. The same data should not be present in both train and validation files. |
| `suffix`                                                                                                                                                                                                                                                                                                                                                          | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | A string that will be added to your fine-tuning model name. For example, a suffix of "my-great-model" would produce a model name like `ft:open-mistral-7b:my-great-model:xxx...`                                                                                                                                                                                  |
| `integrations`                                                                                                                                                                                                                                                                                                                                                    | List[[models.JobInIntegrations](../../models/jobinintegrations.md)]                                                                                                                                                                                                                                                                                               | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | A list of integrations to enable for your fine-tuning job.                                                                                                                                                                                                                                                                                                        |
| `auto_start`                                                                                                                                                                                                                                                                                                                                                      | *Optional[bool]*                                                                                                                                                                                                                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | This field will be required in a future release.                                                                                                                                                                                                                                                                                                                  |
| `invalid_sample_skip_percentage`                                                                                                                                                                                                                                                                                                                                  | *Optional[float]*                                                                                                                                                                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | N/A                                                                                                                                                                                                                                                                                                                                                               |
| `job_type`                                                                                                                                                                                                                                                                                                                                                        | [OptionalNullable[models.FineTuneableModelType]](../../models/finetuneablemodeltype.md)                                                                                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | N/A                                                                                                                                                                                                                                                                                                                                                               |
| `repositories`                                                                                                                                                                                                                                                                                                                                                    | List[[models.JobInRepositories](../../models/jobinrepositories.md)]                                                                                                                                                                                                                                                                                               | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | N/A                                                                                                                                                                                                                                                                                                                                                               |
| `classifier_targets`                                                                                                                                                                                                                                                                                                                                              | List[[models.ClassifierTargetIn](../../models/classifiertargetin.md)]                                                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | N/A                                                                                                                                                                                                                                                                                                                                                               |
| `retries`                                                                                                                                                                                                                                                                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                                               |

### Response

**[models.JobsAPIRoutesFineTuningCreateFineTuningJobResponse](../../models/jobsapiroutesfinetuningcreatefinetuningjobresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## get

Get a fine-tuned job details by its UUID.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_fine_tuning_get_fine_tuning_job" method="get" path="/v1/fine_tuning/jobs/{job_id}" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.fine_tuning.jobs.get(job_id="c167a961-ffca-4bcf-93ac-6169468dd389")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `job_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | The ID of the job to analyse.                                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.JobsAPIRoutesFineTuningGetFineTuningJobResponse](../../models/jobsapiroutesfinetuninggetfinetuningjobresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## cancel

Request the cancellation of a fine tuning job.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_fine_tuning_cancel_fine_tuning_job" method="post" path="/v1/fine_tuning/jobs/{job_id}/cancel" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.fine_tuning.jobs.cancel(job_id="6188a2f6-7513-4e0f-89cc-3f8088523a49")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `job_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | The ID of the job to cancel.                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.JobsAPIRoutesFineTuningCancelFineTuningJobResponse](../../models/jobsapiroutesfinetuningcancelfinetuningjobresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## start

Request the start of a validated fine tuning job.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_fine_tuning_start_fine_tuning_job" method="post" path="/v1/fine_tuning/jobs/{job_id}/start" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.fine_tuning.jobs.start(job_id="56553e4d-0679-471e-b9ac-59a77d671103")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `job_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.JobsAPIRoutesFineTuningStartFineTuningJobResponse](../../models/jobsapiroutesfinetuningstartfinetuningjobresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |