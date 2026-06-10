# UpdateDocumentRequest


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `name`                                                               | *Optional[str]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `attributes`                                                         | Dict[str, [models.AttributesUnion](../models/attributesunion.md)]    | :heavy_minus_sign:                                                   | N/A                                                                  |
| `expires_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | If set, the document will be automatically deleted after this date.  |