# Models

## Overview

Model Management API

### Available Operations

* [update](#update) - Update Fine Tuned Model
* [archive](#archive) - Archive Fine Tuned Model
* [unarchive](#unarchive) - Unarchive Fine Tuned Model

## update

Update a model name or description.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_fine_tuning_update_fine_tuned_model" method="patch" path="/v1/fine_tuning/models/{model_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.models.update(model_id="ft:open-mistral-7b:587a6b29:20240514:7e773925")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `model_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The ID of the model to update.                                      | ft:open-mistral-7b:587a6b29:20240514:7e773925                       |
| `name`                                                              | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `description`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.JobsAPIRoutesFineTuningUpdateFineTunedModelResponse](../../models/jobsapiroutesfinetuningupdatefinetunedmodelresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## archive

Archive a fine-tuned model.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_fine_tuning_archive_fine_tuned_model" method="post" path="/v1/fine_tuning/models/{model_id}/archive" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.models.archive(model_id="ft:open-mistral-7b:587a6b29:20240514:7e773925")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `model_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The ID of the model to archive.                                     | ft:open-mistral-7b:587a6b29:20240514:7e773925                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.ArchiveModelResponse](../../models/archivemodelresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## unarchive

Un-archive a fine-tuned model.

### Example Usage

<!-- UsageSnippet language="python" operationID="jobs_api_routes_fine_tuning_unarchive_fine_tuned_model" method="delete" path="/v1/fine_tuning/models/{model_id}/archive" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.models.unarchive(model_id="ft:open-mistral-7b:587a6b29:20240514:7e773925")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `model_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The ID of the model to unarchive.                                   | ft:open-mistral-7b:587a6b29:20240514:7e773925                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.UnarchiveModelResponse](../../models/unarchivemodelresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |