# DeploymentLocation


## Fields

| Field                                            | Type                                             | Required                                         | Description                                      |
| ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ |
| `location_type`                                  | [models.LocationType](../models/locationtype.md) | :heavy_check_mark:                               | N/A                                              |
| `k8s_cluster`                                    | *OptionalNullable[str]*                          | :heavy_minus_sign:                               | K8s cluster name, if applicable                  |
| `k8s_namespace`                                  | *OptionalNullable[str]*                          | :heavy_minus_sign:                               | K8s namespace, if applicable                     |