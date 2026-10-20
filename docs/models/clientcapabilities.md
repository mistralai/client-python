# ClientCapabilities

Capabilities a client may support.

Not a closed set: any client can define additional capabilities. Sent once in
`initialize` through 2025-11-25; per-request in `_meta` on 2026-07-28.


## Fields

| Field                                                                                | Type                                                                                 | Required                                                                             | Description                                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `experimental`                                                                       | Dict[str, Dict[str, *Any*]]                                                          | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `sampling`                                                                           | [OptionalNullable[models.SamplingCapability]](../models/samplingcapability.md)       | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `elicitation`                                                                        | [OptionalNullable[models.ElicitationCapability]](../models/elicitationcapability.md) | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `roots`                                                                              | [OptionalNullable[models.RootsCapability]](../models/rootscapability.md)             | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `extensions`                                                                         | Dict[str, Dict[str, *Any*]]                                                          | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `tasks`                                                                              | [OptionalNullable[models.ClientTasksCapability]](../models/clienttaskscapability.md) | :heavy_minus_sign:                                                                   | N/A                                                                                  |