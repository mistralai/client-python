from typing import TYPE_CHECKING, Mapping, Optional

from pydantic import BaseModel

from mistralai.client import errors, models, utils
from mistralai.client._hooks.types import HookContext
from mistralai.client.types.basemodel import UNSET, OptionalNullable
from mistralai.client.utils.security import get_security_from_env
from mistralai.client.utils.unmarshal_json_response import unmarshal_json_response

if TYPE_CHECKING:
    from mistralai.client.sdk import Mistral


class WorkerInfo(BaseModel):
    scheduler_url: str
    namespace: str


async def get_scheduler_namespace(
    client: "Mistral",
    *,
    retries: OptionalNullable[utils.RetryConfig] = UNSET,
    server_url: Optional[str] = None,
    timeout_ms: Optional[int] = None,
    http_headers: Optional[Mapping[str, str]] = None,
) -> str:
    base_url = None
    url_variables = None
    if timeout_ms is None:
        timeout_ms = client.sdk_configuration.timeout_ms

    if server_url is not None:
        base_url = server_url
    else:
        base_url = client._get_url(base_url, url_variables)
    req = client._build_request_async(
        method="GET",
        path="/v1/workflows/workers/whoami",
        base_url=base_url,
        url_variables=url_variables,
        request=None,
        request_body_required=False,
        request_has_path_params=False,
        request_has_query_params=True,
        user_agent_header="user-agent",
        accept_header_value="application/json",
        http_headers=http_headers,
        security=client.sdk_configuration.security,
        allow_empty_value=None,
        timeout_ms=timeout_ms,
    )

    if retries == UNSET:
        if client.sdk_configuration.retry_config is not UNSET:
            retries = client.sdk_configuration.retry_config

    retry_config = None
    if isinstance(retries, utils.RetryConfig):
        retry_config = (retries, ["429", "500", "502", "503", "504"])

    http_res = await client.do_request_async(
        hook_ctx=HookContext(
            config=client.sdk_configuration,
            base_url=base_url or "",
            operation_id="get_worker_info_v1_workflows_workers_whoami_get",
            oauth2_scopes=None,
            security_source=get_security_from_env(
                client.sdk_configuration.security, models.Security
            ),
        ),
        request=req,
        error_status_codes=["4XX", "5XX"],
        retry_config=retry_config,
    )

    if utils.match_response(http_res, "200", "application/json"):
        return unmarshal_json_response(WorkerInfo, http_res).namespace
    if utils.match_response(http_res, "4XX", "*"):
        http_res_text = await utils.stream_to_text_async(http_res)
        raise errors.SDKError("API error occurred", http_res, http_res_text)
    if utils.match_response(http_res, "5XX", "*"):
        http_res_text = await utils.stream_to_text_async(http_res)
        raise errors.SDKError("API error occurred", http_res, http_res_text)

    raise errors.SDKError("Unexpected response received", http_res)
