"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from .basesdk import BaseSDK
from mistralai_gcp import models, utils
from mistralai_gcp._hooks import HookContext
from mistralai_gcp.types import OptionalNullable, UNSET
from mistralai_gcp.utils import eventstreaming
from typing import Any, List, Mapping, Optional, Union


class Chat(BaseSDK):
    r"""Chat Completion API."""

    def stream(
        self,
        *,
        model: str,
        messages: Union[List[models.Messages], List[models.MessagesTypedDict]],
        temperature: OptionalNullable[float] = UNSET,
        top_p: Optional[float] = None,
        max_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = True,
        stop: Optional[Union[models.Stop, models.StopTypedDict]] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[
            Union[models.ResponseFormat, models.ResponseFormatTypedDict]
        ] = None,
        tools: OptionalNullable[
            Union[List[models.Tool], List[models.ToolTypedDict]]
        ] = UNSET,
        tool_choice: Optional[
            Union[
                models.ChatCompletionStreamRequestToolChoice,
                models.ChatCompletionStreamRequestToolChoiceTypedDict,
            ]
        ] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        n: OptionalNullable[int] = UNSET,
        prediction: Optional[
            Union[models.Prediction, models.PredictionTypedDict]
        ] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> Optional[eventstreaming.EventStream[models.CompletionEvent]]:
        r"""Stream chat completion

        Mistral AI provides the ability to stream responses back to a client in order to allow partial results for certain requests. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

        :param model: ID of the model to use. You can use the [List Available Models](/api/#tag/models/operation/list_models_v1_models_get) API to see all of your available models, or see our [Model overview](/models) for model descriptions.
        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param temperature: What sampling temperature to use, we recommend between 0.0 and 0.7. Higher values like 0.7 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. The default value varies depending on the model you are targeting. Call the `/models` endpoint to retrieve the appropriate value.
        :param top_p: Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.
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
        :param prediction:
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        :param http_headers: Additional headers to set or replace on requests.
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url
        else:
            base_url = self._get_url(base_url, url_variables)

        request = models.ChatCompletionStreamRequest(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(messages, List[models.Messages]),
            response_format=utils.get_pydantic_model(
                response_format, Optional[models.ResponseFormat]
            ),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(
                tool_choice, Optional[models.ChatCompletionStreamRequestToolChoice]
            ),
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
            prediction=utils.get_pydantic_model(
                prediction, Optional[models.Prediction]
            ),
        )

        req = self._build_request(
            method="POST",
            path="/streamRawPredict",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="text/event-stream",
            http_headers=http_headers,
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request, False, False, "json", models.ChatCompletionStreamRequest
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
                base_url=base_url or "",
                operation_id="stream_chat",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["422", "4XX", "5XX"],
            stream=True,
            retry_config=retry_config,
        )

        response_data: Any = None
        if utils.match_response(http_res, "200", "text/event-stream"):
            return eventstreaming.EventStream(
                http_res,
                lambda raw: utils.unmarshal_json(raw, models.CompletionEvent),
                sentinel="[DONE]",
            )
        if utils.match_response(http_res, "422", "application/json"):
            http_res_text = utils.stream_to_text(http_res)
            response_data = utils.unmarshal_json(
                http_res_text, models.HTTPValidationErrorData
            )
            raise models.HTTPValidationError(data=response_data)
        if utils.match_response(http_res, "4XX", "*"):
            http_res_text = utils.stream_to_text(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )
        if utils.match_response(http_res, "5XX", "*"):
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
        model: str,
        messages: Union[List[models.Messages], List[models.MessagesTypedDict]],
        temperature: OptionalNullable[float] = UNSET,
        top_p: Optional[float] = None,
        max_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = True,
        stop: Optional[Union[models.Stop, models.StopTypedDict]] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[
            Union[models.ResponseFormat, models.ResponseFormatTypedDict]
        ] = None,
        tools: OptionalNullable[
            Union[List[models.Tool], List[models.ToolTypedDict]]
        ] = UNSET,
        tool_choice: Optional[
            Union[
                models.ChatCompletionStreamRequestToolChoice,
                models.ChatCompletionStreamRequestToolChoiceTypedDict,
            ]
        ] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        n: OptionalNullable[int] = UNSET,
        prediction: Optional[
            Union[models.Prediction, models.PredictionTypedDict]
        ] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> Optional[eventstreaming.EventStreamAsync[models.CompletionEvent]]:
        r"""Stream chat completion

        Mistral AI provides the ability to stream responses back to a client in order to allow partial results for certain requests. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

        :param model: ID of the model to use. You can use the [List Available Models](/api/#tag/models/operation/list_models_v1_models_get) API to see all of your available models, or see our [Model overview](/models) for model descriptions.
        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param temperature: What sampling temperature to use, we recommend between 0.0 and 0.7. Higher values like 0.7 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. The default value varies depending on the model you are targeting. Call the `/models` endpoint to retrieve the appropriate value.
        :param top_p: Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.
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
        :param prediction:
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        :param http_headers: Additional headers to set or replace on requests.
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url
        else:
            base_url = self._get_url(base_url, url_variables)

        request = models.ChatCompletionStreamRequest(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(messages, List[models.Messages]),
            response_format=utils.get_pydantic_model(
                response_format, Optional[models.ResponseFormat]
            ),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(
                tool_choice, Optional[models.ChatCompletionStreamRequestToolChoice]
            ),
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
            prediction=utils.get_pydantic_model(
                prediction, Optional[models.Prediction]
            ),
        )

        req = self._build_request_async(
            method="POST",
            path="/streamRawPredict",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="text/event-stream",
            http_headers=http_headers,
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request, False, False, "json", models.ChatCompletionStreamRequest
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
                base_url=base_url or "",
                operation_id="stream_chat",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["422", "4XX", "5XX"],
            stream=True,
            retry_config=retry_config,
        )

        response_data: Any = None
        if utils.match_response(http_res, "200", "text/event-stream"):
            return eventstreaming.EventStreamAsync(
                http_res,
                lambda raw: utils.unmarshal_json(raw, models.CompletionEvent),
                sentinel="[DONE]",
            )
        if utils.match_response(http_res, "422", "application/json"):
            http_res_text = await utils.stream_to_text_async(http_res)
            response_data = utils.unmarshal_json(
                http_res_text, models.HTTPValidationErrorData
            )
            raise models.HTTPValidationError(data=response_data)
        if utils.match_response(http_res, "4XX", "*"):
            http_res_text = await utils.stream_to_text_async(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )
        if utils.match_response(http_res, "5XX", "*"):
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

    def complete(
        self,
        *,
        model: str,
        messages: Union[
            List[models.ChatCompletionRequestMessages],
            List[models.ChatCompletionRequestMessagesTypedDict],
        ],
        temperature: OptionalNullable[float] = UNSET,
        top_p: Optional[float] = None,
        max_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = False,
        stop: Optional[
            Union[
                models.ChatCompletionRequestStop,
                models.ChatCompletionRequestStopTypedDict,
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
                models.ChatCompletionRequestToolChoice,
                models.ChatCompletionRequestToolChoiceTypedDict,
            ]
        ] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        n: OptionalNullable[int] = UNSET,
        prediction: Optional[
            Union[models.Prediction, models.PredictionTypedDict]
        ] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> Optional[models.ChatCompletionResponse]:
        r"""Chat Completion

        :param model: ID of the model to use. You can use the [List Available Models](/api/#tag/models/operation/list_models_v1_models_get) API to see all of your available models, or see our [Model overview](/models) for model descriptions.
        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param temperature: What sampling temperature to use, we recommend between 0.0 and 0.7. Higher values like 0.7 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. The default value varies depending on the model you are targeting. Call the `/models` endpoint to retrieve the appropriate value.
        :param top_p: Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.
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
        :param prediction:
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        :param http_headers: Additional headers to set or replace on requests.
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url
        else:
            base_url = self._get_url(base_url, url_variables)

        request = models.ChatCompletionRequest(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(
                messages, List[models.ChatCompletionRequestMessages]
            ),
            response_format=utils.get_pydantic_model(
                response_format, Optional[models.ResponseFormat]
            ),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(
                tool_choice, Optional[models.ChatCompletionRequestToolChoice]
            ),
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
            prediction=utils.get_pydantic_model(
                prediction, Optional[models.Prediction]
            ),
        )

        req = self._build_request(
            method="POST",
            path="/rawPredict",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            http_headers=http_headers,
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request, False, False, "json", models.ChatCompletionRequest
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
                base_url=base_url or "",
                operation_id="chat_completion_v1_chat_completions_post",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["422", "4XX", "5XX"],
            retry_config=retry_config,
        )

        response_data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(
                http_res.text, Optional[models.ChatCompletionResponse]
            )
        if utils.match_response(http_res, "422", "application/json"):
            response_data = utils.unmarshal_json(
                http_res.text, models.HTTPValidationErrorData
            )
            raise models.HTTPValidationError(data=response_data)
        if utils.match_response(http_res, "4XX", "*"):
            http_res_text = utils.stream_to_text(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )
        if utils.match_response(http_res, "5XX", "*"):
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
        model: str,
        messages: Union[
            List[models.ChatCompletionRequestMessages],
            List[models.ChatCompletionRequestMessagesTypedDict],
        ],
        temperature: OptionalNullable[float] = UNSET,
        top_p: Optional[float] = None,
        max_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = False,
        stop: Optional[
            Union[
                models.ChatCompletionRequestStop,
                models.ChatCompletionRequestStopTypedDict,
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
                models.ChatCompletionRequestToolChoice,
                models.ChatCompletionRequestToolChoiceTypedDict,
            ]
        ] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        n: OptionalNullable[int] = UNSET,
        prediction: Optional[
            Union[models.Prediction, models.PredictionTypedDict]
        ] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> Optional[models.ChatCompletionResponse]:
        r"""Chat Completion

        :param model: ID of the model to use. You can use the [List Available Models](/api/#tag/models/operation/list_models_v1_models_get) API to see all of your available models, or see our [Model overview](/models) for model descriptions.
        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param temperature: What sampling temperature to use, we recommend between 0.0 and 0.7. Higher values like 0.7 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. The default value varies depending on the model you are targeting. Call the `/models` endpoint to retrieve the appropriate value.
        :param top_p: Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.
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
        :param prediction:
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        :param http_headers: Additional headers to set or replace on requests.
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url
        else:
            base_url = self._get_url(base_url, url_variables)

        request = models.ChatCompletionRequest(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(
                messages, List[models.ChatCompletionRequestMessages]
            ),
            response_format=utils.get_pydantic_model(
                response_format, Optional[models.ResponseFormat]
            ),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(
                tool_choice, Optional[models.ChatCompletionRequestToolChoice]
            ),
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
            prediction=utils.get_pydantic_model(
                prediction, Optional[models.Prediction]
            ),
        )

        req = self._build_request_async(
            method="POST",
            path="/rawPredict",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            http_headers=http_headers,
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request, False, False, "json", models.ChatCompletionRequest
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
                base_url=base_url or "",
                operation_id="chat_completion_v1_chat_completions_post",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["422", "4XX", "5XX"],
            retry_config=retry_config,
        )

        response_data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(
                http_res.text, Optional[models.ChatCompletionResponse]
            )
        if utils.match_response(http_res, "422", "application/json"):
            response_data = utils.unmarshal_json(
                http_res.text, models.HTTPValidationErrorData
            )
            raise models.HTTPValidationError(data=response_data)
        if utils.match_response(http_res, "4XX", "*"):
            http_res_text = await utils.stream_to_text_async(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )
        if utils.match_response(http_res, "5XX", "*"):
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
