# DeploymentKoyebBackendSpec

Worker configuration for the Koyeb backend.


## Fields

| Field                                                                            | Type                                                                             | Required                                                                         | Description                                                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `type`                                                                           | *Literal["koyeb"]*                                                               | :heavy_check_mark:                                                               | N/A                                                                              |
| `build_directory`                                                                | *OptionalNullable[str]*                                                          | :heavy_minus_sign:                                                               | Docker build context, as a path in the repo. Defaults to the repo root.          |
| `dockerfile_path`                                                                | *OptionalNullable[str]*                                                          | :heavy_minus_sign:                                                               | Path to the Dockerfile, relative to 'build_directory'. Defaults to 'Dockerfile'. |