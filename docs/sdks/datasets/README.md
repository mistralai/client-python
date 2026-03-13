# Beta.Observability.Datasets

## Overview

(beta) Manage conversation datasets

### Available Operations

* [create](#create) - Create a new empty dataset
* [list](#list) - List existing datasets
* [fetch](#fetch) - Get dataset by id
* [delete](#delete) - Delete a dataset
* [update](#update) - Patch dataset
* [list_records](#list_records) - List existing records in the dataset
* [create_record](#create_record) - Add a conversation to the dataset
* [import_from_campaign](#import_from_campaign) - Populate the dataset with a campaign
* [import_from_explorer](#import_from_explorer) - Populate the dataset with samples from the explorer
* [import_from_file](#import_from_file) - Populate the dataset with samples from an uploaded file
* [import_from_playground](#import_from_playground) - Populate the dataset with samples from the playground
* [import_from_dataset_records](#import_from_dataset_records) - Populate the dataset with samples from another dataset
* [export_to_jsonl](#export_to_jsonl) - Export to the Files API and retrieve presigned URL to download the resulting JSONL file
* [fetch_task](#fetch_task) - Get status of a dataset import task
* [list_tasks](#list_tasks) - List import tasks for the given dataset

## create

Create a new empty dataset

### Example Usage

<!-- UsageSnippet language="python" operationID="create_dataset_v1_observability_datasets_post" method="post" path="/v1/observability/datasets" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.create(name="<value>", description="citizen whoever sustenance necessary vibrant openly")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `description`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Dataset](../../models/dataset.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## list

List existing datasets

### Example Usage

<!-- UsageSnippet language="python" operationID="get_datasets_v1_observability_datasets_get" method="get" path="/v1/observability/datasets" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.list(page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `q`                                                                 | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetPreviews](../../models/datasetpreviews.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch

Get dataset by id

### Example Usage

<!-- UsageSnippet language="python" operationID="get_dataset_by_id_v1_observability_datasets__dataset_id__get" method="get" path="/v1/observability/datasets/{dataset_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.fetch(dataset_id="036fa362-e080-4fa5-beff-a334a70efb58")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetPreview](../../models/datasetpreview.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## delete

Delete a dataset

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_dataset_v1_observability_datasets__dataset_id__delete" method="delete" path="/v1/observability/datasets/{dataset_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.datasets.delete(dataset_id="baf961a3-bb8e-4085-89ef-de9c5d8c4e77")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## update

Patch dataset

### Example Usage

<!-- UsageSnippet language="python" operationID="update_dataset_v1_observability_datasets__dataset_id__patch" method="patch" path="/v1/observability/datasets/{dataset_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.update(dataset_id="95be9afc-fc05-44a6-af9f-2362de1224f9")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `name`                                                              | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `description`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetPreview](../../models/datasetpreview.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## list_records

List existing records in the dataset

### Example Usage

<!-- UsageSnippet language="python" operationID="get_dataset_records_v1_observability_datasets__dataset_id__records_get" method="get" path="/v1/observability/datasets/{dataset_id}/records" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.list_records(dataset_id="444d2a88-e636-4bc0-ab6c-919bedaed112", page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetRecords](../../models/datasetrecords.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## create_record

Add a conversation to the dataset

### Example Usage

<!-- UsageSnippet language="python" operationID="create_dataset_record_v1_observability_datasets__dataset_id__records_post" method="post" path="/v1/observability/datasets/{dataset_id}/records" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.create_record(dataset_id="4c54ed13-1459-44e1-8696-1a6df06f7177", payload=models.ConversationPayload(
        messages=[
            {
                "key": "<value>",
            },
            {
                "key": "<value>",
                "key1": "<value>",
            },
        ],
    ), properties={
        "key": "<value>",
        "key1": "<value>",
        "key2": "<value>",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `payload`                                                           | [models.ConversationPayload](../../models/conversationpayload.md)   | :heavy_check_mark:                                                  | N/A                                                                 |
| `properties`                                                        | Dict[str, *Any*]                                                    | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetRecord](../../models/datasetrecord.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## import_from_campaign

Populate the dataset with a campaign

### Example Usage

<!-- UsageSnippet language="python" operationID="post_dataset_records_from_campaign_v1_observability_datasets__dataset_id__imports_from_campaign_post" method="post" path="/v1/observability/datasets/{dataset_id}/imports/from-campaign" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.import_from_campaign(dataset_id="306b5f31-e31c-4e06-9220-e3008c61bf1b", campaign_id="71a2e42d-7414-4fe6-89cb-44a2122b6f6b")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `campaign_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetImportTask](../../models/datasetimporttask.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## import_from_explorer

Populate the dataset with samples from the explorer

### Example Usage

<!-- UsageSnippet language="python" operationID="post_dataset_records_from_explorer_v1_observability_datasets__dataset_id__imports_from_explorer_post" method="post" path="/v1/observability/datasets/{dataset_id}/imports/from-explorer" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.import_from_explorer(dataset_id="ee1930e9-54f7-4c68-aa8a-40fe5d2a3485", completion_event_ids=[
        "<value 1>",
        "<value 2>",
        "<value 3>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `completion_event_ids`                                              | List[*str*]                                                         | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetImportTask](../../models/datasetimporttask.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## import_from_file

Populate the dataset with samples from an uploaded file

### Example Usage

<!-- UsageSnippet language="python" operationID="post_dataset_records_from_file_v1_observability_datasets__dataset_id__imports_from_file_post" method="post" path="/v1/observability/datasets/{dataset_id}/imports/from-file" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.import_from_file(dataset_id="1c96c925-cc58-4529-863d-9fe66a6f1924", file_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetImportTask](../../models/datasetimporttask.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## import_from_playground

Populate the dataset with samples from the playground

### Example Usage

<!-- UsageSnippet language="python" operationID="post_dataset_records_from_playground_v1_observability_datasets__dataset_id__imports_from_playground_post" method="post" path="/v1/observability/datasets/{dataset_id}/imports/from-playground" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.import_from_playground(dataset_id="5cb42584-5fcf-4837-997a-6a67c5e6900d", conversation_ids=[])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `conversation_ids`                                                  | List[*str*]                                                         | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetImportTask](../../models/datasetimporttask.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## import_from_dataset_records

Populate the dataset with samples from another dataset

### Example Usage

<!-- UsageSnippet language="python" operationID="post_dataset_records_from_dataset_v1_observability_datasets__dataset_id__imports_from_dataset_post" method="post" path="/v1/observability/datasets/{dataset_id}/imports/from-dataset" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.import_from_dataset_records(dataset_id="ada96a08-d724-4e5c-9111-aaf1bdb7d588", dataset_record_ids=[
        "58fe798a-537b-4c61-9efc-d1d96d5d264a",
        "cfa1d197-deda-456e-906b-dd84dccfcd17",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `dataset_record_ids`                                                | List[*str*]                                                         | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetImportTask](../../models/datasetimporttask.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## export_to_jsonl

Export to the Files API and retrieve presigned URL to download the resulting JSONL file

### Example Usage

<!-- UsageSnippet language="python" operationID="export_dataset_to_jsonl_v1_observability_datasets__dataset_id__exports_to_jsonl_get" method="get" path="/v1/observability/datasets/{dataset_id}/exports/to-jsonl" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.export_to_jsonl(dataset_id="d521add6-d909-4a69-a460-cb880d87b773")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetExport](../../models/datasetexport.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch_task

Get status of a dataset import task

### Example Usage

<!-- UsageSnippet language="python" operationID="get_dataset_import_task_v1_observability_datasets__dataset_id__tasks__task_id__get" method="get" path="/v1/observability/datasets/{dataset_id}/tasks/{task_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.fetch_task(dataset_id="b64b504e-58a2-4d52-979b-e2634b301235", task_id="1713cde2-dea1-410d-851e-8cea964ffa14")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `task_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetImportTask](../../models/datasetimporttask.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## list_tasks

List import tasks for the given dataset

### Example Usage

<!-- UsageSnippet language="python" operationID="get_dataset_import_tasks_v1_observability_datasets__dataset_id__tasks_get" method="get" path="/v1/observability/datasets/{dataset_id}/tasks" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.datasets.list_tasks(dataset_id="29903443-7f9c-42a6-9b6b-fc5cbef4191a", page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DatasetImportTasks](../../models/datasetimporttasks.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |