# RunOptimizationRef

Typed run→optimization back-ref, derived at read from the optimization_run link.

Not stored on the run (single source of truth = optimization_run); lets a run row show
its optimization (id + name) without an extra request per run.


## Fields

| Field              | Type               | Required           | Description        |
| ------------------ | ------------------ | ------------------ | ------------------ |
| `optimization_id`  | *str*              | :heavy_check_mark: | N/A                |
| `name`             | *str*              | :heavy_check_mark: | N/A                |