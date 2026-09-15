# TempoGetTraceResponse

Trace response in OpenTelemetry format.

This is the unified trace format used across all trace providers (Tempo, ClickHouse, etc.).
Regardless of the underlying backend, all trace data is normalized to this Tempo-compatible
OpenTelemetry format to ensure consistency in the API response structure.


## Fields

| Field                                                        | Type                                                         | Required                                                     | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `batches`                                                    | List[[models.TempoTraceBatch](../models/tempotracebatch.md)] | :heavy_minus_sign:                                           | The batches of the trace                                     |