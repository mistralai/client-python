# RetrieveFileOut


## Fields

| Field                                          | Type                                           | Required                                       | Description                                    | Example                                        |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |
| `id`                                           | *str*                                          | :heavy_check_mark:                             | The unique identifier of the file.             | 497f6eca-6276-4993-bfeb-53cbbbba6f09           |
| `object`                                       | *str*                                          | :heavy_check_mark:                             | The object type, which is always "file".       | file                                           |
| `bytes`                                        | *int*                                          | :heavy_check_mark:                             | The size of the file, in bytes.                | 13000                                          |
| `created_at`                                   | *int*                                          | :heavy_check_mark:                             | The UNIX timestamp (in seconds) of the event.  | 1716963433                                     |
| `filename`                                     | *str*                                          | :heavy_check_mark:                             | The name of the uploaded file.                 | files_upload.jsonl                             |
| `purpose`                                      | [models.FilePurpose](../models/filepurpose.md) | :heavy_check_mark:                             | N/A                                            |                                                |
| `sample_type`                                  | [models.SampleType](../models/sampletype.md)   | :heavy_check_mark:                             | N/A                                            |                                                |
| `source`                                       | [models.Source](../models/source.md)           | :heavy_check_mark:                             | N/A                                            |                                                |
| `deleted`                                      | *bool*                                         | :heavy_check_mark:                             | N/A                                            |                                                |
| `num_lines`                                    | *OptionalNullable[int]*                        | :heavy_minus_sign:                             | N/A                                            |                                                |