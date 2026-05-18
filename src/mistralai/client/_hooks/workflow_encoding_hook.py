import asyncio
import concurrent.futures
import json
import logging
import re
import uuid
import weakref
from typing import Any, AsyncIterator, Coroutine, Dict, Optional, TypeVar, Union

import httpx
from httpx._types import AsyncByteStream

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
    def __init__(self, payload_encoder: PayloadEncoder, namespace: str) -> None:
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


def _get_encoding_config(
    sdk_config: SDKConfiguration,
) -> Optional[_WorkflowEncodingConfig]:
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

# Operations that return event data that may need decryption
OPERATIONS_DECODE_EVENTS = {
    "get_workflow_events_v1_workflows_events_list_get",
}

# Streaming operations that return SSE event data that may need decryption
OPERATIONS_DECODE_EVENTS_STREAM = {
    "get_stream_events_v1_workflows_events_stream_get",
    "stream_v1_workflows_executions__execution_id__stream_get",
}

SCHEDULE_CORRELATION_ID_PLACEHOLDER = "__scheduled_workflow__"


def _is_payload_type(value: Any) -> bool:
    """Check if a value is a JSONPayload or JSONPatchPayload by its structure.

    Payload types have: {"type": "json" | "json_patch", "value": ...}
    """
    if not isinstance(value, dict):
        return False
    payload_type = value.get("type")
    return payload_type in ("json", "json_patch") and "value" in value


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


async def _decrypt_event_attributes(
    attributes: Dict[str, Any],
    payload_encoder: PayloadEncoder,
) -> Dict[str, Any]:
    """Decrypt payload fields in event attributes."""
    for field_name, field_value in attributes.items():
        if not _is_payload_type(field_value):
            continue

        # Check if it has encoding_options (meaning it's encrypted)
        if not field_value.get("encoding_options"):
            continue

        # Decrypt the payload
        decrypted = await payload_encoder.decode_event_payload(field_value)
        attributes[field_name] = decrypted

    return attributes


async def _decrypt_events_in_response(
    body: Dict[str, Any],
    payload_encoder: PayloadEncoder,
) -> Dict[str, Any]:
    """Decrypt payload fields in events within a response body."""
    events = body.get("events", [])
    if not events:
        return body

    for event in events:
        attributes = event.get("attributes")
        if isinstance(attributes, dict):
            event["attributes"] = await _decrypt_event_attributes(
                attributes, payload_encoder
            )

    return body


def _decrypt_sse_line(line: bytes, payload_encoder: PayloadEncoder) -> bytes:
    """Decrypt event payloads in an SSE data line."""
    if not line.startswith(b"data:"):
        return line

    try:
        data_part = line[5:].strip()
        if not data_part:
            return line

        event_wrapper = json.loads(data_part)
        data = event_wrapper.get("data")
        if not isinstance(data, dict):
            return line

        attributes = data.get("attributes")
        if not isinstance(attributes, dict):
            return line

        # Decrypt in place - _decrypt_event_attributes modifies attributes dict
        _run_async(_decrypt_event_attributes(attributes, payload_encoder))

        return b"data: " + json.dumps(event_wrapper).encode("utf-8")
    except (json.JSONDecodeError, Exception) as e:
        logger.debug("SSE line decryption failed: %s", e)
        return line


class _DecryptingAsyncByteStream(AsyncByteStream):
    """Async byte stream wrapper that decrypts SSE event payloads."""

    def __init__(self, original_stream: Any, payload_encoder: PayloadEncoder):
        self._original = original_stream
        self._payload_encoder = payload_encoder
        self._buffer = b""

    async def __aiter__(self) -> AsyncIterator[bytes]:
        async for chunk in self._original:
            for processed in self._process_chunk(chunk):
                yield processed
        # Flush remaining buffer
        if self._buffer:
            yield _decrypt_sse_line(self._buffer, self._payload_encoder)

    def _process_chunk(self, chunk: bytes):
        self._buffer += chunk
        lines = self._buffer.split(b"\n")
        # Keep last incomplete line in buffer
        self._buffer = lines[-1]
        for line in lines[:-1]:
            yield _decrypt_sse_line(line, self._payload_encoder) + b"\n"

    async def aclose(self) -> None:
        if hasattr(self._original, "aclose"):
            await self._original.aclose()


def _wrap_sse_response_with_decryption(
    response: httpx.Response,
    payload_encoder: PayloadEncoder,
) -> httpx.Response:
    """Wrap an SSE response to decrypt event payloads as they stream.

    Creates a new response with a custom stream that decrypts payloads on-the-fly.
    """
    # Get the original stream from the response
    original_stream = response.stream

    # Create wrapped stream
    decrypting_stream = _DecryptingAsyncByteStream(original_stream, payload_encoder)

    # Create new response with wrapped stream
    # Use internal _content to avoid reading stream
    new_response = httpx.Response(
        status_code=response.status_code,
        headers=response.headers,
        stream=decrypting_stream,
        request=response.request,
        extensions=response.extensions,
    )

    return new_response


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

            encoded_input = _run_async(
                encoding_config.payload_encoder.encode_network_input(
                    input_data, context
                )
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
        """Intercept responses to decode workflow result payloads and event payloads."""
        encoding_config = _get_encoding_config(hook_ctx.config)
        if not encoding_config:
            return response

        content_type = response.headers.get("content-type", "")

        # Handle SSE stream decryption
        if hook_ctx.operation_id in OPERATIONS_DECODE_EVENTS_STREAM:
            if "text/event-stream" in content_type:
                return _wrap_sse_response_with_decryption(
                    response, encoding_config.payload_encoder
                )
            return response

        if "application/json" not in content_type:
            return response

        # Handle workflow result decoding
        if hook_ctx.operation_id in OPERATIONS_DECODE_RESULT:
            try:
                body = json.loads(response.content)
                result = body.get("result")
                if (
                    result is not None
                    and encoding_config.payload_encoder.check_is_payload_encoded(
                        result
                    )
                ):
                    decoded_result = _run_async(
                        encoding_config.payload_encoder.decode_network_result(result)
                    )

                    body["result"] = decoded_result
                    new_content = json.dumps(body).encode("utf-8")

                    response = httpx.Response(
                        status_code=response.status_code,
                        headers=response.headers,
                        content=new_content,
                        request=response.request,
                        extensions=response.extensions,
                    )
            except Exception as e:
                logger.error("WorkflowEncodingHook: Failed to decode result: %s", e)
                raise

        # Handle event payload decoding
        elif hook_ctx.operation_id in OPERATIONS_DECODE_EVENTS:
            try:
                body = json.loads(response.content)
                body = _run_async(
                    _decrypt_events_in_response(body, encoding_config.payload_encoder)
                )
                new_content = json.dumps(body).encode("utf-8")

                response = httpx.Response(
                    status_code=response.status_code,
                    headers=response.headers,
                    content=new_content,
                    request=response.request,
                    extensions=response.extensions,
                )
            except Exception as e:
                logger.error("WorkflowEncodingHook: Failed to decode events: %s", e)
                raise

        return response
