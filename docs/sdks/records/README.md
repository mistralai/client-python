# Beta.Observability.Datasets.Records

## Overview

### Available Operations

* [fetch](#fetch) - Get the content of a given conversation from a dataset
* [delete](#delete) - Delete a record from a dataset
* [bulk_delete](#bulk_delete) - Delete multiple records from datasets
* [judge](#judge) - Run Judge on a dataset record based on the given options
* [update_payload](#update_payload) - Update a dataset record conversation payload
* [update_properties](#update_properties) - Update conversation properties

## fetch

Get the content of a given conversation from a dataset

### Example Usage

<!-- UsageSnippet language="python" operationID="get_dataset_record_v1_observability_dataset_records__dataset_record_id__get" method="get" path="/v1/observability/dataset-records/{dataset_record_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.records.fetch(dataset_record_id="ce995349-abbf-45c0-be75-885fc1c4b4c0")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_record_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetRecord](../../models/datasetrecord.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## delete

Delete a record from a dataset

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_dataset_record_v1_observability_dataset_records__dataset_record_id__delete" method="delete" path="/v1/observability/dataset-records/{dataset_record_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.datasets.records.delete(dataset_record_id="799fed99-80b4-4a9a-a15e-05352b811702")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_record_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## bulk_delete

Delete multiple records from datasets

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_dataset_records_v1_observability_dataset_records_bulk_delete_post" method="post" path="/v1/observability/dataset-records/bulk-delete" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.datasets.records.bulk_delete(dataset_record_ids=[
        "22fc78f7-e774-4ab5-b1ea-63852992ef31",
        "1c533b4f-882e-4bd0-9ef6-9933b825f8b1",
    ])

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_record_ids`                                                | List[*str*]                                                         | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## judge

Run Judge on a dataset record based on the given options

### Example Usage

<!-- UsageSnippet language="python" operationID="judge_dataset_record_v1_observability_dataset_records__dataset_record_id__live_judging_post" method="post" path="/v1/observability/dataset-records/{dataset_record_id}/live-judging" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.records.judge(dataset_record_id="9de5d7a1-787a-45dd-b668-9f3407e76d8b", judge_definition={
        "name": "<value>",
        "description": "wisely railway deceivingly arcade minion back what yowza outrun service",
        "model_name": "<value>",
        "output": {
            "type": "CLASSIFICATION",
            "options": [
                {
                    "value": "<value>",
                    "description": "spork excluding without retrospectivity bah next yearly",
                },
            ],
        },
        "instructions": "<value>",
        "tools": [
            "<value 1>",
        ],
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_record_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `judge_definition`                                                  | [models.CreateJudgeRequest](../../models/createjudgerequest.md)     | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.JudgeOutput](../../models/judgeoutput.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## update_payload

Update a dataset record conversation payload

### Example Usage

<!-- UsageSnippet language="python" operationID="update_dataset_record_payload_v1_observability_dataset_records__dataset_record_id__payload_put" method="put" path="/v1/observability/dataset-records/{dataset_record_id}/payload" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.datasets.records.update_payload(dataset_record_id="17506b15-748e-4e7c-9737-c97c44d04b0f", payload=models.ConversationPayload(
        messages=[
            {
                "key": "<value>",
            },
            {

            },
            {
                "key": "<value>",
            },
        ],
    ))

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_record_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `payload`                                                           | [models.ConversationPayload](../../models/conversationpayload.md)   | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## update_properties

Update conversation properties

### Example Usage

<!-- UsageSnippet language="python" operationID="update_dataset_record_properties_v1_observability_dataset_records__dataset_record_id__properties_put" method="put" path="/v1/observability/dataset-records/{dataset_record_id}/properties" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.datasets.records.update_properties(dataset_record_id="a4deefc5-0905-427e-ad15-1090ef9e216d", properties={
        "key": "<value>",
        "key1": "<value>",
        "key2": "<value>",
    })

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_record_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `properties`                                                        | Dict[str, *Any*]                                                    | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |