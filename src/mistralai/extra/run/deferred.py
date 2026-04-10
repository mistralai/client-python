"""Helper functions for processing deferred tool call responses.

Moved out of conversations.py to avoid conflicts with speakeasy code generation,
which overwrites everything outside custom regions.
"""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

from mistralai.client import models
from mistralai.extra.exceptions import (
    DeferralReason,
    DeferredToolCallConfirmation,
    DeferredToolCallRejection,
    DeferredToolCallResponse,
    RunException,
)

if TYPE_CHECKING:
    from mistralai.extra.run.context import RunContext


def _is_deferred_response(obj) -> bool:
    """Check if object is a DeferredToolResponse."""
    return isinstance(obj, (DeferredToolCallConfirmation, DeferredToolCallRejection))


def _is_server_deferred(fc: models.FunctionCallEntry) -> bool:
    """Check if a function call was deferred server-side (pending confirmation)."""
    return getattr(fc, "confirmation_status", None) == "pending"


async def _process_deferred_responses(
    run_ctx: "RunContext",
    responses: list[DeferredToolCallResponse],
) -> tuple[list[models.InputEntries], list[models.ToolCallConfirmation]]:
    """Process deferred tool responses and return function results and server-side confirmations.

    For client-side deferrals (CONFIRMATION_REQUIRED):
      - Confirmations: executes the tool using run_ctx -> FunctionResultEntry
      - Rejections: creates a result with the rejection message -> FunctionResultEntry
    For server-side deferrals (SERVER_SIDE_CONFIRMATION_REQUIRED):
      - Confirmations: returns ToolCallConfirmation(confirmation="allow")
      - Rejections: returns ToolCallConfirmation(confirmation="deny")
    """
    results: list[models.InputEntries] = []
    tool_confirmations: list[models.ToolCallConfirmation] = []
    confirmation_tasks: list[tuple[str, str, asyncio.Task]] = []

    for response in responses:
        if isinstance(response, DeferredToolCallConfirmation):
            reason = getattr(
                response, "deferral_reason", DeferralReason.CONFIRMATION_REQUIRED
            )

            if reason == DeferralReason.SERVER_SIDE_CONFIRMATION_REQUIRED:
                tool_confirmations.append(
                    models.ToolCallConfirmation(
                        tool_call_id=response.tool_call_id,
                        confirmation="allow",
                    )
                )
            else:
                if response.override_args is not None:
                    original_args = (
                        json.loads(response.function_call.arguments)
                        if isinstance(response.function_call.arguments, str)
                        else response.function_call.arguments
                    )
                    merged_args = {**original_args, **response.override_args}
                    function_call = models.FunctionCallEntry(
                        id=response.function_call.id,
                        tool_call_id=response.tool_call_id,
                        name=response.tool_name,
                        arguments=json.dumps(merged_args),
                    )
                else:
                    function_call = response.function_call

                task = asyncio.create_task(
                    run_ctx.execute_function_calls([function_call])
                )
                confirmation_tasks.append(
                    (response.tool_call_id, response.tool_name, task)
                )

        elif isinstance(response, DeferredToolCallRejection):
            reason = getattr(
                response, "deferral_reason", DeferralReason.CONFIRMATION_REQUIRED
            )

            if reason == DeferralReason.SERVER_SIDE_CONFIRMATION_REQUIRED:
                tool_confirmations.append(
                    models.ToolCallConfirmation(
                        tool_call_id=response.tool_call_id,
                        confirmation="deny",
                    )
                )
            else:
                results.append(
                    models.FunctionResultEntry(
                        tool_call_id=response.tool_call_id,
                        result=response.message,
                    )
                )

    if confirmation_tasks:
        await asyncio.gather(*[task for _, _, task in confirmation_tasks])
        for tool_call_id, tool_name, task in confirmation_tasks:
            task_results = task.result()
            if task_results:
                results.append(task_results[0])
            else:
                raise RunException(
                    f"Tool '{tool_name}' is not registered in the RunContext"
                )

    return results, tool_confirmations
