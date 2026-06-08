# V1Metadata


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `created_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `last_modified_at`                                                   | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `latest_version`                                                     | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | Version number of the latest version of this object.                 |
| `name`                                                               | *Optional[str]*                                                      | :heavy_minus_sign:                                                   | Optional human-readable name (immutable after creation).             |
| `sharing_scope`                                                      | [Optional[models.V1SharingScope]](../models/v1sharingscope.md)       | :heavy_minus_sign:                                                   | N/A                                                                  |
| `created_by`                                                         | *Optional[str]*                                                      | :heavy_minus_sign:                                                   | User ID of the creator. Immutable after creation.                    |