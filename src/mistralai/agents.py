"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from .basesdk import BaseSDK
from mistralai import models, utils
from mistralai._hooks import HookContext
from mistralai.types import OptionalNullable, UNSET
from mistralai.utils import eventstreaming, get_security_from_env
from typing import Any, AsyncGenerator, Generator, List, Optional, Union


class Agents(BaseSDK):
    r"""Agents API."""

    def complete(
        self,
        *,
        messages: Union[
            List[models.AgentsCompletionRequestMessages],
            List[models.AgentsCompletionRequestMessagesTypedDict],
        ],
        agent_id: str,
        max_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = False,
        stop: Optional[
            Union[
                models.AgentsCompletionRequestStop,
                models.AgentsCompletionRequestStopTypedDict,
            ]
        ] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[
            Union[models.ResponseFormat, models.ResponseFormatTypedDict]
        ] = None,
        tools: OptionalNullable[
            Union[List[models.Tool], List[models.ToolTypedDict]]
        ] = UNSET,
        tool_choice: Optional[
            Union[
                models.AgentsCompletionRequestToolChoice,
                models.AgentsCompletionRequestToolChoiceTypedDict,
            ]
        ] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        n: OptionalNullable[int] = UNSET,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[models.ChatCompletionResponse]:
        r"""Agents Completion

        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param agent_id: The ID of the agent to use for this completion.
        :param max_tokens: The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.
        :param stream: Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.
        :param stop: Stop generation if this token is detected. Or if one of these tokens is detected when providing an array
        :param random_seed: The seed to use for random sampling. If set, different calls will generate deterministic results.
        :param response_format:
        :param tools:
        :param tool_choice:
        :param presence_penalty: presence_penalty determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative.
        :param frequency_penalty: frequency_penalty penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition.
        :param n: Number of completions to return for each request, input tokens are only billed once.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = models.AgentsCompletionRequest(
            max_tokens=max_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(
                messages, List[models.AgentsCompletionRequestMessages]
            ),
            response_format=utils.get_pydantic_model(
                response_format, Optional[models.ResponseFormat]
            ),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(
                tool_choice, Optional[models.AgentsCompletionRequestToolChoice]
            ),
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
            agent_id=agent_id,
        )

        req = self.build_request(
            method="POST",
            path="/v1/agents/completions",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request, False, False, "json", models.AgentsCompletionRequest
            ),
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = self.do_request(
            hook_ctx=HookContext(
                operation_id="agents_completion_v1_agents_completions_post",
                oauth2_scopes=[],
                security_source=get_security_from_env(
                    self.sdk_configuration.security, models.Security
                ),
            ),
            request=req,
            error_status_codes=["422", "4XX", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(
                http_res.text, Optional[models.ChatCompletionResponse]
            )
        if utils.match_response(http_res, "422", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.HTTPValidationErrorData)
            raise models.HTTPValidationError(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            http_res_text = utils.stream_to_text(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )

        content_type = http_res.headers.get("Content-Type")
        http_res_text = utils.stream_to_text(http_res)
        raise models.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res_text,
            http_res,
        )

    async def complete_async(
        self,
        *,
        messages: Union[
            List[models.AgentsCompletionRequestMessages],
            List[models.AgentsCompletionRequestMessagesTypedDict],
        ],
        agent_id: str,
        max_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = False,
        stop: Optional[
            Union[
                models.AgentsCompletionRequestStop,
                models.AgentsCompletionRequestStopTypedDict,
            ]
        ] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[
            Union[models.ResponseFormat, models.ResponseFormatTypedDict]
        ] = None,
        tools: OptionalNullable[
            Union[List[models.Tool], List[models.ToolTypedDict]]
        ] = UNSET,
        tool_choice: Optional[
            Union[
                models.AgentsCompletionRequestToolChoice,
                models.AgentsCompletionRequestToolChoiceTypedDict,
            ]
        ] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        n: OptionalNullable[int] = UNSET,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[models.ChatCompletionResponse]:
        r"""Agents Completion

        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param agent_id: The ID of the agent to use for this completion.
        :param max_tokens: The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.
        :param stream: Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.
        :param stop: Stop generation if this token is detected. Or if one of these tokens is detected when providing an array
        :param random_seed: The seed to use for random sampling. If set, different calls will generate deterministic results.
        :param response_format:
        :param tools:
        :param tool_choice:
        :param presence_penalty: presence_penalty determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative.
        :param frequency_penalty: frequency_penalty penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition.
        :param n: Number of completions to return for each request, input tokens are only billed once.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = models.AgentsCompletionRequest(
            max_tokens=max_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(
                messages, List[models.AgentsCompletionRequestMessages]
            ),
            response_format=utils.get_pydantic_model(
                response_format, Optional[models.ResponseFormat]
            ),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(
                tool_choice, Optional[models.AgentsCompletionRequestToolChoice]
            ),
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
            agent_id=agent_id,
        )

        req = self.build_request_async(
            method="POST",
            path="/v1/agents/completions",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request, False, False, "json", models.AgentsCompletionRequest
            ),
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = await self.do_request_async(
            hook_ctx=HookContext(
                operation_id="agents_completion_v1_agents_completions_post",
                oauth2_scopes=[],
                security_source=get_security_from_env(
                    self.sdk_configuration.security, models.Security
                ),
            ),
            request=req,
            error_status_codes=["422", "4XX", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(
                http_res.text, Optional[models.ChatCompletionResponse]
            )
        if utils.match_response(http_res, "422", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.HTTPValidationErrorData)
            raise models.HTTPValidationError(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            http_res_text = await utils.stream_to_text_async(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )

        content_type = http_res.headers.get("Content-Type")
        http_res_text = await utils.stream_to_text_async(http_res)
        raise models.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res_text,
            http_res,
        )

    def stream(
        self,
        *,
        messages: Union[
            List[models.AgentsCompletionStreamRequestMessages],
            List[models.AgentsCompletionStreamRequestMessagesTypedDict],
        ],
        agent_id: str,
        max_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = True,
        stop: Optional[
            Union[
                models.AgentsCompletionStreamRequestStop,
                models.AgentsCompletionStreamRequestStopTypedDict,
            ]
        ] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[
            Union[models.ResponseFormat, models.ResponseFormatTypedDict]
        ] = None,
        tools: OptionalNullable[
            Union[List[models.Tool], List[models.ToolTypedDict]]
        ] = UNSET,
        tool_choice: Optional[
            Union[
                models.AgentsCompletionStreamRequestToolChoice,
                models.AgentsCompletionStreamRequestToolChoiceTypedDict,
            ]
        ] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        n: OptionalNullable[int] = UNSET,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[Generator[models.CompletionEvent, None, None]]:
        r"""Stream Agents completion

        Mistral AI provides the ability to stream responses back to a client in order to allow partial results for certain requests. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param agent_id: The ID of the agent to use for this completion.
        :param max_tokens: The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.
        :param stream:
        :param stop: Stop generation if this token is detected. Or if one of these tokens is detected when providing an array
        :param random_seed: The seed to use for random sampling. If set, different calls will generate deterministic results.
        :param response_format:
        :param tools:
        :param tool_choice:
        :param presence_penalty: presence_penalty determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative.
        :param frequency_penalty: frequency_penalty penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition.
        :param n: Number of completions to return for each request, input tokens are only billed once.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = models.AgentsCompletionStreamRequest(
            max_tokens=max_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(
                messages, List[models.AgentsCompletionStreamRequestMessages]
            ),
            response_format=utils.get_pydantic_model(
                response_format, Optional[models.ResponseFormat]
            ),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(
                tool_choice, Optional[models.AgentsCompletionStreamRequestToolChoice]
            ),
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
            agent_id=agent_id,
        )

        req = self.build_request(
            method="POST",
            path="/v1/agents/completions#stream",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="text/event-stream",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request, False, False, "json", models.AgentsCompletionStreamRequest
            ),
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = self.do_request(
            hook_ctx=HookContext(
                operation_id="stream_agents",
                oauth2_scopes=[],
                security_source=get_security_from_env(
                    self.sdk_configuration.security, models.Security
                ),
            ),
            request=req,
            error_status_codes=["422", "4XX", "5XX"],
            stream=True,
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "text/event-stream"):
            return eventstreaming.stream_events(
                http_res,
                lambda raw: utils.unmarshal_json(raw, models.CompletionEvent),
                sentinel="[DONE]",
            )
        if utils.match_response(http_res, "422", "application/json"):
            http_res_text = utils.stream_to_text(http_res)
            data = utils.unmarshal_json(http_res_text, models.HTTPValidationErrorData)
            raise models.HTTPValidationError(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            http_res_text = utils.stream_to_text(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )

        content_type = http_res.headers.get("Content-Type")
        http_res_text = utils.stream_to_text(http_res)
        raise models.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res_text,
            http_res,
        )

    async def stream_async(
        self,
        *,
        messages: Union[
            List[models.AgentsCompletionStreamRequestMessages],
            List[models.AgentsCompletionStreamRequestMessagesTypedDict],
        ],
        agent_id: str,
        max_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = True,
        stop: Optional[
            Union[
                models.AgentsCompletionStreamRequestStop,
                models.AgentsCompletionStreamRequestStopTypedDict,
            ]
        ] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[
            Union[models.ResponseFormat, models.ResponseFormatTypedDict]
        ] = None,
        tools: OptionalNullable[
            Union[List[models.Tool], List[models.ToolTypedDict]]
        ] = UNSET,
        tool_choice: Optional[
            Union[
                models.AgentsCompletionStreamRequestToolChoice,
                models.AgentsCompletionStreamRequestToolChoiceTypedDict,
            ]
        ] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        n: OptionalNullable[int] = UNSET,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[AsyncGenerator[models.CompletionEvent, None]]:
        r"""Stream Agents completion

        Mistral AI provides the ability to stream responses back to a client in order to allow partial results for certain requests. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param agent_id: The ID of the agent to use for this completion.
        :param max_tokens: The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.
        :param stream:
        :param stop: Stop generation if this token is detected. Or if one of these tokens is detected when providing an array
        :param random_seed: The seed to use for random sampling. If set, different calls will generate deterministic results.
        :param response_format:
        :param tools:
        :param tool_choice:
        :param presence_penalty: presence_penalty determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative.
        :param frequency_penalty: frequency_penalty penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition.
        :param n: Number of completions to return for each request, input tokens are only billed once.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = models.AgentsCompletionStreamRequest(
            max_tokens=max_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(
                messages, List[models.AgentsCompletionStreamRequestMessages]
            ),
            response_format=utils.get_pydantic_model(
                response_format, Optional[models.ResponseFormat]
            ),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(
                tool_choice, Optional[models.AgentsCompletionStreamRequestToolChoice]
            ),
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
            agent_id=agent_id,
        )

        req = self.build_request_async(
            method="POST",
            path="/v1/agents/completions#stream",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="text/event-stream",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request, False, False, "json", models.AgentsCompletionStreamRequest
            ),
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = await self.do_request_async(
            hook_ctx=HookContext(
                operation_id="stream_agents",
                oauth2_scopes=[],
                security_source=get_security_from_env(
                    self.sdk_configuration.security, models.Security
                ),
            ),
            request=req,
            error_status_codes=["422", "4XX", "5XX"],
            stream=True,
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "text/event-stream"):
            return eventstreaming.stream_events_async(
                http_res,
                lambda raw: utils.unmarshal_json(raw, models.CompletionEvent),
                sentinel="[DONE]",
            )
        if utils.match_response(http_res, "422", "application/json"):
            http_res_text = await utils.stream_to_text_async(http_res)
            data = utils.unmarshal_json(http_res_text, models.HTTPValidationErrorData)
            raise models.HTTPValidationError(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            http_res_text = await utils.stream_to_text_async(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )

        content_type = http_res.headers.get("Content-Type")
        http_res_text = await utils.stream_to_text_async(http_res)
        raise models.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res_text,
            http_res,
        )
