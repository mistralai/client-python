# VespaIndexInput


## Fields

| Field                                                          | Type                                                           | Required                                                       | Description                                                    |
| -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| `type`                                                         | *Literal["vespa"]*                                             | :heavy_check_mark:                                             | N/A                                                            |
| `k8s_cluster`                                                  | *str*                                                          | :heavy_check_mark:                                             | N/A                                                            |
| `k8s_namespace`                                                | *str*                                                          | :heavy_check_mark:                                             | N/A                                                            |
| `vespa_instance_name`                                          | *str*                                                          | :heavy_check_mark:                                             | N/A                                                            |
| `vespa_version`                                                | *str*                                                          | :heavy_check_mark:                                             | N/A                                                            |
| `schemas`                                                      | List[[models.VespaSchemaInput](../models/vespaschemainput.md)] | :heavy_check_mark:                                             | N/A                                                            |
| `query_url`                                                    | *str*                                                          | :heavy_check_mark:                                             | N/A                                                            |