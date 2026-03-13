# ResponseToEvaluatePayload

The messages should be a list of "DeltaMessage", but this class hides
that so that it can be used in the {In|Out}Schema classes to avoid
leaking mistral-common's data model in the OpenAPI spec.


## Fields

| Field                  | Type                   | Required               | Description            |
| ---------------------- | ---------------------- | ---------------------- | ---------------------- |
| `messages`             | List[Dict[str, *Any*]] | :heavy_check_mark:     | N/A                    |