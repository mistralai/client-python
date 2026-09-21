# TempoTraceEvent


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `name`                                                               | *str*                                                                | :heavy_check_mark:                                                   | The name of the event                                                |
| `time_unix_nano`                                                     | *str*                                                                | :heavy_check_mark:                                                   | The time of the event in Unix nano                                   |
| `attributes`                                                         | List[[models.TempoTraceAttribute](../models/tempotraceattribute.md)] | :heavy_minus_sign:                                                   | The attributes of the event                                          |