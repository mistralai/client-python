import asyncio
import concurrent.futures
import json
import logging
import re
import uuid
import weakref
from typing import Any, Coroutine, Dict, Optional, TypeVar, Union

import httpx

from .types import (
    AfterSuccessContext,
    AfterSuccessHook,
    BeforeRequestContext,
    BeforeRequestHook,
)
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.extra.workflows.encoding.config import WorkflowEncodingConfig
from mistralai.extra.workflows.encoding.helpers import generate_two_part_id
from mistralai.extra.workflows.encoding.models import WorkflowContext
from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder

logger = logging.getLogger(__name__)

# Attribute name for storing config ID on SDKConfiguration
_ENCODING_CONFIG_ID_ATTR = "_workflow_encoding_config_id"


class _WorkflowEncodingConfig:
    def __init__(
        self, payload_encoder: PayloadEncoder, namespace: str
    ) -> None:
        self.payload_encoder = payload_encoder
        self.namespace = namespace


# Per-client configs keyed by UUID
_workflow_configs: Dict[str, _WorkflowEncodingConfig] = {}


def _cleanup_config(config_id: str) -> None:
    """Remove config when client is garbage collected."""
    _workflow_configs.pop(config_id, None)


def configure_workflow_encoding(
    config: WorkflowEncodingConfig,
    namespace: str,
    sdk_config: SDKConfiguration,
) -> None:
    """Configure workflow payload encoding for a specific client."""
    # Get or create config ID for this client
    config_id = getattr(sdk_config, _ENCODING_CONFIG_ID_ATTR, None)
    if config_id is None:
        config_id = str(uuid.uuid4())
        setattr(sdk_config, _ENCODING_CONFIG_ID_ATTR, config_id)
        # Register cleanup when SDKConfiguration is garbage collected
        weakref.finalize(sdk_config, _cleanup_config, config_id)

    _workflow_configs[config_id] = _WorkflowEncodingConfig(
        payload_encoder=PayloadEncoder(encoding_config=config),
        namespace=namespace,
    )


def _get_encoding_config(sdk_config: SDKConfiguration) -> Optional[_WorkflowEncodingConfig]:
    """Get workflow encoding config for a client."""
    config_id = getattr(sdk_config, _ENCODING_CONFIG_ID_ATTR, None)
    if config_id is None:
        return None
    return _workflow_configs.get(config_id)


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


_T = TypeVar("_T")


def _run_async(coro: Coroutine[Any, Any, _T]) -> _T:
    """Run an async coroutine in a sync context."""
    try:
        asyncio.get_running_loop()
        # Already in async context - run in a separate thread with new loop
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future: concurrent.futures.Future[_T] = pool.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        # No running loop - safe to use asyncio.run
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
        encoding_config = _get_encoding_config(hook_ctx.config)
        if not encoding_config:
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
                execution_id = generate_two_part_id(seed)
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
                namespace=encoding_config.namespace,
                execution_id=execution_id,
            )

            logger.debug(
                "WorkflowEncodingHook: Encoding input for %s", hook_ctx.operation_id
            )

            encoded_input = _run_async(
                encoding_config.payload_encoder.encode_network_input(input_data, context)
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
        encoding_config = _get_encoding_config(hook_ctx.config)
        if not encoding_config:
            return response

        if hook_ctx.operation_id not in OPERATIONS_DECODE_RESULT:
            return response

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return response

        try:
            body = json.loads(response.content)
            result = body.get("result")
            if result is None or not encoding_config.payload_encoder.check_is_payload_encoded(result):
                return response

            logger.debug(
                "WorkflowEncodingHook: Decoding result for %s", hook_ctx.operation_id
            )

            decoded_result = _run_async(encoding_config.payload_encoder.decode_network_result(result))

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
