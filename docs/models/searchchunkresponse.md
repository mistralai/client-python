# SearchChunkResponse

Wire chunk: atom fields plus any custom fields (via ``extra``).


## Fields

| Field                   | Type                    | Required                | Description             |
| ----------------------- | ----------------------- | ----------------------- | ----------------------- |
| `id`                    | *str*                   | :heavy_check_mark:      | N/A                     |
| `source_id`             | *str*                   | :heavy_check_mark:      | N/A                     |
| `locator`               | *str*                   | :heavy_check_mark:      | N/A                     |
| `start_offset`          | *Nullable[int]*         | :heavy_check_mark:      | N/A                     |
| `end_offset`            | *Nullable[int]*         | :heavy_check_mark:      | N/A                     |
| `chunk_type`            | *str*                   | :heavy_check_mark:      | N/A                     |
| `parent_ref`            | *OptionalNullable[str]* | :heavy_minus_sign:      | N/A                     |
| `content`               | *str*                   | :heavy_check_mark:      | N/A                     |
| `metadata`              | Dict[str, *Any*]        | :heavy_minus_sign:      | N/A                     |
| `__pydantic_extra__`    | Dict[str, *Any*]        | :heavy_minus_sign:      | N/A                     |