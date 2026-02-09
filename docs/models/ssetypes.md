# SSETypes

Server side events sent when streaming a conversation response.


## Values

| Name                            | Value                           |
| ------------------------------- | ------------------------------- |
| `CONVERSATION_RESPONSE_STARTED` | conversation.response.started   |
| `CONVERSATION_RESPONSE_DONE`    | conversation.response.done      |
| `CONVERSATION_RESPONSE_ERROR`   | conversation.response.error     |
| `MESSAGE_OUTPUT_DELTA`          | message.output.delta            |
| `TOOL_EXECUTION_STARTED`        | tool.execution.started          |
| `TOOL_EXECUTION_DELTA`          | tool.execution.delta            |
| `TOOL_EXECUTION_DONE`           | tool.execution.done             |
| `AGENT_HANDOFF_STARTED`         | agent.handoff.started           |
| `AGENT_HANDOFF_DONE`            | agent.handoff.done              |
| `FUNCTION_CALL_DELTA`           | function.call.delta             |