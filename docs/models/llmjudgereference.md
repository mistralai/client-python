# LlmJudgeReference

The scorer selected to build a judge pipeline configuration.


## Fields

| Field                                                                                  | Type                                                                                   | Required                                                                               | Description                                                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `slug`                                                                                 | *str*                                                                                  | :heavy_check_mark:                                                                     | N/A                                                                                    |
| `mapping`                                                                              | Dict[str, *str*]                                                                       | :heavy_minus_sign:                                                                     | N/A                                                                                    |
| `sampling`                                                                             | [OptionalNullable[models.PipelineConfigSampling]](../models/pipelineconfigsampling.md) | :heavy_minus_sign:                                                                     | N/A                                                                                    |