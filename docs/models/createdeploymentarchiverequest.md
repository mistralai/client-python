# CreateDeploymentArchiveRequest

The size of the gzipped tar a managed deployment will build from.


## Fields

| Field                                                                                        | Type                                                                                         | Required                                                                                     | Description                                                                                  |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `size`                                                                                       | *int*                                                                                        | :heavy_check_mark:                                                                           | Size of the gzipped tar in bytes, at most 256 MiB. The upload URL accepts exactly this size. |