# ExecutionTraceInfoResponse


## Fields

| Field                                                                   | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `otel_trace_id`                                                         | *OptionalNullable[str]*                                                 | :heavy_minus_sign:                                                      | The ID of the trace, if available                                       |
| `has_trace_data`                                                        | *Optional[bool]*                                                        | :heavy_minus_sign:                                                      | Whether trace data is available in the trace backend for this execution |