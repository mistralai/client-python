# Beta.Observability.Evaluations.Runs

## Overview

(beta) Start or retrieve an evaluation run

### Available Operations

* [create](#create) - Run an evaluation
* [list](#list) - Get evaluation runs
* [list_records](#list_records) - Get evaluation records for the given evaluation run id
* [generate_responses_and_judgements](#generate_responses_and_judgements) - Start generating the model responses to evaluate using an agent and evaluate them with a judge
* [generate_responses_to_evaluate_with_agent](#generate_responses_to_evaluate_with_agent) - Start generating the model responses to evaluate using an agent
* [generate_judgements_with_judge](#generate_judgements_with_judge) - Start judging the responses using an LLM judge
* [upload_responses_to_evaluate](#upload_responses_to_evaluate) - Upload responses to evaluate
* [upload_judgements](#upload_judgements) - Upload judgements for each response to evaluate
* [fetch_status](#fetch_status) - Get evaluation run status by evaluation id
* [fetch_metrics](#fetch_metrics) - Get evaluation run metrics
* [delete](#delete) - Delete an evaluation run

## create

Run an evaluation

### Example Usage

<!-- UsageSnippet language="python" operationID="create_evaluation_run_v1_observability_evaluations__evaluation_id__runs_post" method="post" path="/v1/observability/evaluations/{evaluation_id}/runs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.create(evaluation_id="1b4e492a-9316-40a7-8216-2c064bb5273c")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_id`                                                     | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.EvaluationRun](../../models/evaluationrun.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## list

Get evaluation runs

### Example Usage

<!-- UsageSnippet language="python" operationID="get_evaluation_runs_v1_observability_evaluations__evaluation_id__runs_get" method="get" path="/v1/observability/evaluations/{evaluation_id}/runs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.list(evaluation_id="4614e9b6-e142-4756-b1cd-eb5f0db2bd2a", page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_id`                                                     | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.EvaluationRuns](../../models/evaluationruns.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## list_records

Get evaluation records for the given evaluation run id

### Example Usage

<!-- UsageSnippet language="python" operationID="get_evaluation_run_records_v1_observability_evaluation_runs__evaluation_run_id__records_get" method="get" path="/v1/observability/evaluation-runs/{evaluation_run_id}/records" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.list_records(evaluation_run_id="2d615ef5-e694-4fa8-a5b7-b02a9971d8e5", page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_run_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.EvaluationRecords](../../models/evaluationrecords.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## generate_responses_and_judgements

Start generating the model responses to evaluate using an agent and evaluate them with a judge

### Example Usage

<!-- UsageSnippet language="python" operationID="start_generating_responses_to_evaluate_and_judgements_v1_observability_evaluation_runs__evaluation_run_id__responses_to_evaluate_and_judgements_generation_post" method="post" path="/v1/observability/evaluation-runs/{evaluation_run_id}/responses-to-evaluate-and-judgements/generation" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.generate_responses_and_judgements(evaluation_run_id="f79593f3-bab8-464a-8510-284cdf5b06fa", judge_id="b9575897-839c-4c5c-a9fe-5762d75777f5", agent_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_run_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `judge_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## generate_responses_to_evaluate_with_agent

Start generating the model responses to evaluate using an agent

### Example Usage

<!-- UsageSnippet language="python" operationID="start_generating_responses_to_evaluate_v1_observability_evaluation_runs__evaluation_run_id__responses_to_evaluate_generation_post" method="post" path="/v1/observability/evaluation-runs/{evaluation_run_id}/responses-to-evaluate/generation" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.generate_responses_to_evaluate_with_agent(evaluation_run_id="b665c9e8-0d82-4ec8-aa26-29115405c8b4", agent_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_run_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## generate_judgements_with_judge

Start judging the responses using an LLM judge

### Example Usage

<!-- UsageSnippet language="python" operationID="start_judging_records_v1_observability_evaluation_runs__evaluation_run_id__judgements_generation_post" method="post" path="/v1/observability/evaluation-runs/{evaluation_run_id}/judgements/generation" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.generate_judgements_with_judge(evaluation_run_id="777ceccb-888d-4828-a621-0af013a6ea93", judge_id="14a816b0-f320-46bc-9e95-a7759a333e53")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_run_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `judge_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## upload_responses_to_evaluate

Upload responses to evaluate

### Example Usage

<!-- UsageSnippet language="python" operationID="upload_responses_to_evaluate_v1_observability_evaluation_runs__evaluation_run_id__responses_to_evaluate_upload_post" method="post" path="/v1/observability/evaluation-runs/{evaluation_run_id}/responses-to-evaluate/upload" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.upload_responses_to_evaluate(evaluation_run_id="c22bb311-c903-4950-a69a-8a55ca33598e", response_to_evaluate_per_evaluation_record_id={

    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                | Type                                                                                     | Required                                                                                 | Description                                                                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `evaluation_run_id`                                                                      | *str*                                                                                    | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `response_to_evaluate_per_evaluation_record_id`                                          | Dict[str, [models.ResponseToEvaluatePayload](../../models/responsetoevaluatepayload.md)] | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `retries`                                                                                | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                         | :heavy_minus_sign:                                                                       | Configuration to override the default retry behavior of the client.                      |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## upload_judgements

Upload judgements for each response to evaluate

### Example Usage

<!-- UsageSnippet language="python" operationID="upload_judgements_v1_observability_evaluation_runs__evaluation_run_id__judgements_upload_post" method="post" path="/v1/observability/evaluation-runs/{evaluation_run_id}/judgements/upload" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.upload_judgements(evaluation_run_id="df864dcd-220b-439c-bc71-f89209bba637", judgement_per_evaluation_record_id={
        "key": {},
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                              | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `evaluation_run_id`                                                    | *str*                                                                  | :heavy_check_mark:                                                     | N/A                                                                    |
| `judgement_per_evaluation_record_id`                                   | Dict[str, [models.JudgementPayload](../../models/judgementpayload.md)] | :heavy_check_mark:                                                     | N/A                                                                    |
| `retries`                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)       | :heavy_minus_sign:                                                     | Configuration to override the default retry behavior of the client.    |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch_status

Get evaluation run status by evaluation id

### Example Usage

<!-- UsageSnippet language="python" operationID="get_evaluation_run_status_by_id_v1_observability_evaluation_runs__evaluation_run_id__status_get" method="get" path="/v1/observability/evaluation-runs/{evaluation_run_id}/status" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.fetch_status(evaluation_run_id="eccb660b-0ca5-4a04-8fc1-776e0c8c3878")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_run_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.EvaluationRunStatus](../../models/evaluationrunstatus.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch_metrics

Get evaluation run metrics

### Example Usage

<!-- UsageSnippet language="python" operationID="get_evaluation_run_metrics_v1_observability_evaluation_runs__evaluation_run_id__metrics_get" method="get" path="/v1/observability/evaluation-runs/{evaluation_run_id}/metrics" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.fetch_metrics(evaluation_run_id="ed60b9ae-362f-4cb6-9312-0212f7aa1e10")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_run_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ResponseGetEvaluationRunMetricsV1ObservabilityEvaluationRunsEvaluationRunIDMetricsGet](../../models/responsegetevaluationrunmetricsv1observabilityevaluationrunsevaluationrunidmetricsget.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## delete

Delete an evaluation run

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_evaluation_run_v1_observability_evaluation_runs__evaluation_run_id__delete" method="delete" path="/v1/observability/evaluation-runs/{evaluation_run_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.evaluations.runs.delete(evaluation_run_id="ce219df9-8922-4450-a0f2-bddbe76e3bb9")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_run_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |