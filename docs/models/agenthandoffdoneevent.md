# AgentHandoffDoneEvent


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `type`                                                               | *Literal["agent.handoff.done"]*                                      | :heavy_check_mark:                                                   | N/A                                                                  |
| `created_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `output_index`                                                       | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `id`                                                                 | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `next_agent_id`                                                      | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `next_agent_name`                                                    | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |