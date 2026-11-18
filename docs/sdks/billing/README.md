# Beta.Billing

## Overview

### Available Operations

* [get_budget](#get_budget) - Get Budget
* [get_subscription](#get_subscription) - Get Subscription

## get_budget

Return the organization's API and Vibe budgets for the current billing period.

Requires the `see_org_inference_usage` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="billing_api_public_get_budget" method="get" path="/v1/billing/budget" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral() as mistral:

    res = mistral.beta.billing.get_budget(security=models.BillingAPIPublicGetBudgetSecurity(
        dashboard_context_auth=os.getenv("MISTRAL_DASHBOARD_CONTEXT_AUTH", ""),
    ))

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                              | Type                                                                                   | Required                                                                               | Description                                                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `security`                                                                             | [models.BillingAPIPublicGetBudgetSecurity](../../billingapipublicgetbudgetsecurity.md) | :heavy_check_mark:                                                                     | The security requirements to use for the request.                                      |
| `retries`                                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                       | :heavy_minus_sign:                                                                     | Configuration to override the default retry behavior of the client.                    |

### Response

**[models.GetBudgetResponse](../../models/getbudgetresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get_subscription

Return the organization's plan and whether pay-as-you-go is enabled.

### Example Usage

<!-- UsageSnippet language="python" operationID="billing_api_public_get_subscription" method="get" path="/v1/billing/subscription" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral() as mistral:

    res = mistral.beta.billing.get_subscription(security=models.BillingAPIPublicGetSubscriptionSecurity(
        dashboard_context_auth=os.getenv("MISTRAL_DASHBOARD_CONTEXT_AUTH", ""),
    ))

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                          | Type                                                                                               | Required                                                                                           | Description                                                                                        |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `security`                                                                                         | [models.BillingAPIPublicGetSubscriptionSecurity](../../billingapipublicgetsubscriptionsecurity.md) | :heavy_check_mark:                                                                                 | The security requirements to use for the request.                                                  |
| `retries`                                                                                          | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                   | :heavy_minus_sign:                                                                                 | Configuration to override the default retry behavior of the client.                                |

### Response

**[models.GetSubscriptionResponse](../../models/getsubscriptionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |