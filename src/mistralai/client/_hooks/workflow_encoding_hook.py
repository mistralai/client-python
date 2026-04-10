import asyncio
import concurrent.futures
import json
import logging
import re
from typing import Any, Dict, Optional, Union
import uuid

import httpx

from .types import (
    AfterSuccessContext,
    AfterSuccessHook,
    BeforeRequestContext,
    BeforeRequestHook,
)
from mistralai.extra.workflows.encoding.config import WorkflowEncodingConfig
from mistralai.extra.workflows.encoding.models import WorkflowContext
from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder

logger = logging.getLogger(__name__)


class _WorkflowEncodingConfig:
    def __init__(self) -> None:
        self.payload_encoder: Optional[PayloadEncoder] = None
        self.namespace: Optional[str] = None


_workflow_config = _WorkflowEncodingConfig()


def configure_workflow_encoding(
    config: WorkflowEncodingConfig,
    namespace: str,
) -> None:
    """Configure workflow payload encoding by creating a PayloadEncoder.
    """
    _workflow_config.payload_encoder = PayloadEncoder(
        offloading_config=config.payload_offloading,
        encryption_config=config.payload_encryption,
    )
    _workflow_config.namespace = namespace


def get_workflow_payload_encoder() -> Optional[PayloadEncoder]:
    """Get the current workflow payload encoder."""
    return _workflow_config.payload_encoder


def get_workflow_namespace() -> Optional[str]:
    """Get the configured workflow namespace."""
    return _workflow_config.namespace


EXECUTE_WORKFLOW_OPERATION_ID = (
    "execute_workflow_v1_workflows__workflow_identifier__execute_post"
)
EXECUTE_WORKFLOW_REGISTRATION_OPERATION_ID = "execute_workflow_registration_v1_workflows_registrations__workflow_registration_id__execute_post"
SCHEDULE_WORKFLOW_OPERATION_ID = "schedule_workflow_v1_workflows_schedules_post"

EXECUTE_OPERATIONS = {
    EXECUTE_WORKFLOW_OPERATION_ID,
    EXECUTE_WORKFLOW_REGISTRATION_OPERATION_ID,
}

OPERATIONS_ENCODE_INPUT = {
    EXECUTE_WORKFLOW_OPERATION_ID,
    EXECUTE_WORKFLOW_REGISTRATION_OPERATION_ID,
    "signal_workflow_execution_v1_workflows_executions__execution_id__signals_post",
    "query_workflow_execution_v1_workflows_executions__execution_id__queries_post",
    "update_workflow_execution_v1_workflows_executions__execution_id__updates_post",
    SCHEDULE_WORKFLOW_OPERATION_ID,
}

OPERATIONS_DECODE_RESULT = {
    EXECUTE_WORKFLOW_OPERATION_ID,
    EXECUTE_WORKFLOW_REGISTRATION_OPERATION_ID,
    "get_workflow_execution_v1_workflows_executions__execution_id__get",
    "query_workflow_execution_v1_workflows_executions__execution_id__queries_post",
    "update_workflow_execution_v1_workflows_executions__execution_id__updates_post",
}

SCHEDULE_CORRELATION_ID_PLACEHOLDER = "__scheduled_workflow__"


def _run_async(coro: Any) -> Any:
    """Run an async coroutine in a sync context."""
    try:
        asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        return asyncio.run(coro)


def _extract_execution_id_from_url(url: str) -> Optional[str]:
    """Extract execution_id from URL path like /v1/workflows/executions/{execution_id}/..."""
    match = re.search(r"/executions/([^/]+)", str(url))
    if match:
        return match.group(1)
    return None


def _extract_workflow_identifier_from_execute_url(url: str) -> Optional[str]:
    """Extract workflow identifier from execute URLs.

    Handles:
    - /v1/workflows/{workflow_identifier}/execute
    - /v1/workflows/registrations/{workflow_registration_id}/execute
    """
    match = re.search(r"/(?:workflows|registrations)/([^/]+)/execute", str(url))
    return match.group(1) if match else None


def _extract_execution_id_from_body(body: Dict[str, Any]) -> Optional[str]:
    """Extract execution_id from request body."""
    return body.get("execution_id")


def _generate_two_part_id(
    primary_seed: str | None, secondary_seed: str | None = None
) -> str:
    """Generates a unique ID composed of two parts derived from seeds."""
    if not primary_seed:
        primary_seed = uuid.uuid4().hex
    if not secondary_seed:
        secondary_seed = uuid.uuid4().hex
    first_part = uuid.uuid5(uuid.NAMESPACE_DNS, primary_seed).hex
    second_part = uuid.uuid5(uuid.NAMESPACE_DNS, secondary_seed).hex
    return f"{first_part}{second_part}".replace("-", "")


class WorkflowEncodingHook(BeforeRequestHook, AfterSuccessHook):
    """Hook for encoding/decoding workflow event payloads.

    This hook intercepts workflow requests to encode input payloads (encryption,
    blob storage offloading) and decodes result fields in responses.

    Configuration is set via Mistral.configure_workflow_encoding() which initializes
    the PayloadEncoder and stores it at module level.
    """

    def before_request(
        self,
        hook_ctx: BeforeRequestContext,
        request: httpx.Request,
    ) -> Union[httpx.Request, Exception]:
        """Intercept requests to encode workflow input payloads."""
        encoder = get_workflow_payload_encoder()
        namespace = get_workflow_namespace()
        if not encoder or not namespace:
            return request

        if hook_ctx.operation_id not in OPERATIONS_ENCODE_INPUT:
            return request

        content_type = request.headers.get("content-type", "")
        if "application/json" not in content_type:
            return request

        try:
            body = json.loads(request.content)
            input_data = body.get("input")
            if input_data is None:
                return request

            execution_id = _extract_execution_id_from_body(
                body
            ) or _extract_execution_id_from_url(str(request.url))

            if not execution_id and hook_ctx.operation_id in EXECUTE_OPERATIONS:
                seed = _extract_workflow_identifier_from_execute_url(str(request.url))
                execution_id = _generate_two_part_id(seed)
                body["execution_id"] = execution_id

            if (
                not execution_id
                and hook_ctx.operation_id == SCHEDULE_WORKFLOW_OPERATION_ID
            ):
                execution_id = SCHEDULE_CORRELATION_ID_PLACEHOLDER

            if not execution_id:
                raise ValueError(
                    f"WorkflowEncoding: Could not extract execution_id for {hook_ctx.operation_id}"
                )

            context = WorkflowContext(
                namespace=namespace,
                execution_id=execution_id,
            )

            logger.debug(
                "WorkflowEncodingHook: Encoding input for %s", hook_ctx.operation_id
            )

            encoded_input = _run_async(
                encoder.encode_network_input(input_data, context)
            )

            # Update body based on operation type:
            # - Execute operations: use separate `encoded_input` field and set `input` to None
            # - Signal/Query/Update: put encoded input directly in `input` field
            if hook_ctx.operation_id in EXECUTE_OPERATIONS:
                body["encoded_input"] = encoded_input.model_dump(mode="json")
                body["input"] = None
            else:
                body["input"] = encoded_input.model_dump(mode="json")

            new_content = json.dumps(body).encode("utf-8")
            new_headers = httpx.Headers(request.headers)
            new_headers["content-length"] = str(len(new_content))

            return httpx.Request(
                method=request.method,
                url=request.url,
                headers=new_headers,
                content=new_content,
                extensions=request.extensions,
            )

        except Exception as e:
            logger.error("WorkflowEncodingHook: Failed to encode input: %s", e)
            raise

    def after_success(
        self,
        hook_ctx: AfterSuccessContext,
        response: httpx.Response,
    ) -> Union[httpx.Response, Exception]:
        """Intercept responses to decode workflow result payloads."""
        encoder = get_workflow_payload_encoder()
        if not encoder:
            return response

        if hook_ctx.operation_id not in OPERATIONS_DECODE_RESULT:
            return response

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return response

        try:
            body = json.loads(response.content)
            result = body.get("result")
            if result is None or not encoder.check_is_payload_encoded(result):
                return response

            logger.debug(
                "WorkflowEncodingHook: Decoding result for %s", hook_ctx.operation_id
            )

            decoded_result = _run_async(encoder.decode_network_result(result))

            body["result"] = decoded_result
            new_content = json.dumps(body).encode("utf-8")

            return httpx.Response(
                status_code=response.status_code,
                headers=response.headers,
                content=new_content,
                request=response.request,
                extensions=response.extensions,
            )
        except Exception as e:
            logger.error("WorkflowEncodingHook: Failed to decode result: %s", e)
            raise
