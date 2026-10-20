# TransferTarget

One allowed hand-off, chosen by the model through `id` alone.

The address never reaches the model: it only sees `id` and `condition`, so it
cannot dial a near-miss of a real number.


## Fields

| Field                                          | Type                                           | Required                                       | Description                                    |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |
| `id`                                           | *str*                                          | :heavy_check_mark:                             | N/A                                            |
| `condition`                                    | *str*                                          | :heavy_check_mark:                             | N/A                                            |
| `destination`                                  | [models.Destination](../models/destination.md) | :heavy_check_mark:                             | N/A                                            |