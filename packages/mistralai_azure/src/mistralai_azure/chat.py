"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from .basesdk import BaseSDK
from mistralai_azure import models, utils
from mistralai_azure._hooks import HookContext
from mistralai_azure.types import OptionalNullable, UNSET
from mistralai_azure.utils import eventstreaming
from typing import Any, AsyncGenerator, Generator, List, Optional, Union

class Chat(BaseSDK):
    r"""Chat Completion API."""
    
    
    def stream(
        self, *,
        messages: Union[List[models.Messages], List[models.MessagesTypedDict]],
        model: OptionalNullable[str] = "azureai",
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 1,
        max_tokens: OptionalNullable[int] = UNSET,
        min_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = True,
        stop: Optional[Union[models.Stop, models.StopTypedDict]] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[Union[models.ResponseFormat, models.ResponseFormatTypedDict]] = None,
        tools: OptionalNullable[Union[List[models.Tool], List[models.ToolTypedDict]]] = UNSET,
        tool_choice: Optional[Union[models.ChatCompletionStreamRequestToolChoice, models.ChatCompletionStreamRequestToolChoiceTypedDict]] = None,
        safe_prompt: Optional[bool] = False,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[Generator[models.CompletionEvent, None, None]]:
        r"""Stream chat completion

        Mistral AI provides the ability to stream responses back to a client in order to allow partial results for certain requests. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param model: The ID of the model to use for this request.
        :param temperature: What sampling temperature to use, between 0.0 and 1.0. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.
        :param top_p: Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.
        :param max_tokens: The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.
        :param min_tokens: The minimum number of tokens to generate in the completion.
        :param stream: 
        :param stop: Stop generation if this token is detected. Or if one of these tokens is detected when providing an array
        :param random_seed: The seed to use for random sampling. If set, different calls will generate deterministic results.
        :param response_format: 
        :param tools: 
        :param tool_choice: 
        :param safe_prompt: Whether to inject a safety prompt before all conversations.
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
        
        request = models.ChatCompletionStreamRequest(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            min_tokens=min_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(messages, List[models.Messages]),
            response_format=utils.get_pydantic_model(response_format, Optional[models.ResponseFormat]),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(tool_choice, Optional[models.ChatCompletionStreamRequestToolChoice]),
            safe_prompt=safe_prompt,
        )
        
        req = self.build_request(
            method="POST",
            path="/chat/completions#stream",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="text/event-stream",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(request, False, False, "json", models.ChatCompletionStreamRequest),
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = self.do_request(
            hook_ctx=HookContext(operation_id="stream_chat", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["422","4XX","5XX"],
            stream=True,
            retry_config=retry_config
        )
        
        data: Any = None
        if utils.match_response(http_res, "200", "text/event-stream"):
            return eventstreaming.stream_events(http_res, lambda raw: utils.unmarshal_json(raw, models.CompletionEvent), sentinel="[DONE]")
        if utils.match_response(http_res, "422", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.HTTPValidationErrorData)
            raise models.HTTPValidationError(data=data)
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
    
    async def stream_async(
        self, *,
        messages: Union[List[models.Messages], List[models.MessagesTypedDict]],
        model: OptionalNullable[str] = "azureai",
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 1,
        max_tokens: OptionalNullable[int] = UNSET,
        min_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = True,
        stop: Optional[Union[models.Stop, models.StopTypedDict]] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[Union[models.ResponseFormat, models.ResponseFormatTypedDict]] = None,
        tools: OptionalNullable[Union[List[models.Tool], List[models.ToolTypedDict]]] = UNSET,
        tool_choice: Optional[Union[models.ChatCompletionStreamRequestToolChoice, models.ChatCompletionStreamRequestToolChoiceTypedDict]] = None,
        safe_prompt: Optional[bool] = False,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[AsyncGenerator[models.CompletionEvent, None]]:
        r"""Stream chat completion

        Mistral AI provides the ability to stream responses back to a client in order to allow partial results for certain requests. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param model: The ID of the model to use for this request.
        :param temperature: What sampling temperature to use, between 0.0 and 1.0. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.
        :param top_p: Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.
        :param max_tokens: The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.
        :param min_tokens: The minimum number of tokens to generate in the completion.
        :param stream: 
        :param stop: Stop generation if this token is detected. Or if one of these tokens is detected when providing an array
        :param random_seed: The seed to use for random sampling. If set, different calls will generate deterministic results.
        :param response_format: 
        :param tools: 
        :param tool_choice: 
        :param safe_prompt: Whether to inject a safety prompt before all conversations.
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
        
        request = models.ChatCompletionStreamRequest(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            min_tokens=min_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(messages, List[models.Messages]),
            response_format=utils.get_pydantic_model(response_format, Optional[models.ResponseFormat]),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(tool_choice, Optional[models.ChatCompletionStreamRequestToolChoice]),
            safe_prompt=safe_prompt,
        )
        
        req = self.build_request(
            method="POST",
            path="/chat/completions#stream",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="text/event-stream",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(request, False, False, "json", models.ChatCompletionStreamRequest),
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = await self.do_request_async(
            hook_ctx=HookContext(operation_id="stream_chat", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["422","4XX","5XX"],
            stream=True,
            retry_config=retry_config
        )
        
        data: Any = None
        if utils.match_response(http_res, "200", "text/event-stream"):
            return eventstreaming.stream_events_async(http_res, lambda raw: utils.unmarshal_json(raw, models.CompletionEvent), sentinel="[DONE]")
        if utils.match_response(http_res, "422", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.HTTPValidationErrorData)
            raise models.HTTPValidationError(data=data)
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
    
    def complete(
        self, *,
        messages: Union[List[models.ChatCompletionRequestMessages], List[models.ChatCompletionRequestMessagesTypedDict]],
        model: OptionalNullable[str] = "azureai",
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 1,
        max_tokens: OptionalNullable[int] = UNSET,
        min_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = False,
        stop: Optional[Union[models.ChatCompletionRequestStop, models.ChatCompletionRequestStopTypedDict]] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[Union[models.ResponseFormat, models.ResponseFormatTypedDict]] = None,
        tools: OptionalNullable[Union[List[models.Tool], List[models.ToolTypedDict]]] = UNSET,
        tool_choice: Optional[Union[models.ChatCompletionRequestToolChoice, models.ChatCompletionRequestToolChoiceTypedDict]] = None,
        safe_prompt: Optional[bool] = False,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[models.ChatCompletionResponse]:
        r"""Chat Completion

        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param model: The ID of the model to use for this request.
        :param temperature: What sampling temperature to use, between 0.0 and 1.0. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.
        :param top_p: Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.
        :param max_tokens: The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.
        :param min_tokens: The minimum number of tokens to generate in the completion.
        :param stream: Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.
        :param stop: Stop generation if this token is detected. Or if one of these tokens is detected when providing an array
        :param random_seed: The seed to use for random sampling. If set, different calls will generate deterministic results.
        :param response_format: 
        :param tools: 
        :param tool_choice: 
        :param safe_prompt: Whether to inject a safety prompt before all conversations.
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
        
        request = models.ChatCompletionRequest(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            min_tokens=min_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(messages, List[models.ChatCompletionRequestMessages]),
            response_format=utils.get_pydantic_model(response_format, Optional[models.ResponseFormat]),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(tool_choice, Optional[models.ChatCompletionRequestToolChoice]),
            safe_prompt=safe_prompt,
        )
        
        req = self.build_request(
            method="POST",
            path="/chat/completions",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(request, False, False, "json", models.ChatCompletionRequest),
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = self.do_request(
            hook_ctx=HookContext(operation_id="chat_completion_v1_chat_completions_post", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["422","4XX","5XX"],
            retry_config=retry_config
        )
        
        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(http_res.text, Optional[models.ChatCompletionResponse])
        if utils.match_response(http_res, "422", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.HTTPValidationErrorData)
            raise models.HTTPValidationError(data=data)
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
    
    async def complete_async(
        self, *,
        messages: Union[List[models.ChatCompletionRequestMessages], List[models.ChatCompletionRequestMessagesTypedDict]],
        model: OptionalNullable[str] = "azureai",
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 1,
        max_tokens: OptionalNullable[int] = UNSET,
        min_tokens: OptionalNullable[int] = UNSET,
        stream: Optional[bool] = False,
        stop: Optional[Union[models.ChatCompletionRequestStop, models.ChatCompletionRequestStopTypedDict]] = None,
        random_seed: OptionalNullable[int] = UNSET,
        response_format: Optional[Union[models.ResponseFormat, models.ResponseFormatTypedDict]] = None,
        tools: OptionalNullable[Union[List[models.Tool], List[models.ToolTypedDict]]] = UNSET,
        tool_choice: Optional[Union[models.ChatCompletionRequestToolChoice, models.ChatCompletionRequestToolChoiceTypedDict]] = None,
        safe_prompt: Optional[bool] = False,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[models.ChatCompletionResponse]:
        r"""Chat Completion

        :param messages: The prompt(s) to generate completions for, encoded as a list of dict with role and content.
        :param model: The ID of the model to use for this request.
        :param temperature: What sampling temperature to use, between 0.0 and 1.0. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.
        :param top_p: Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.
        :param max_tokens: The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.
        :param min_tokens: The minimum number of tokens to generate in the completion.
        :param stream: Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.
        :param stop: Stop generation if this token is detected. Or if one of these tokens is detected when providing an array
        :param random_seed: The seed to use for random sampling. If set, different calls will generate deterministic results.
        :param response_format: 
        :param tools: 
        :param tool_choice: 
        :param safe_prompt: Whether to inject a safety prompt before all conversations.
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
        
        request = models.ChatCompletionRequest(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            min_tokens=min_tokens,
            stream=stream,
            stop=stop,
            random_seed=random_seed,
            messages=utils.get_pydantic_model(messages, List[models.ChatCompletionRequestMessages]),
            response_format=utils.get_pydantic_model(response_format, Optional[models.ResponseFormat]),
            tools=utils.get_pydantic_model(tools, OptionalNullable[List[models.Tool]]),
            tool_choice=utils.get_pydantic_model(tool_choice, Optional[models.ChatCompletionRequestToolChoice]),
            safe_prompt=safe_prompt,
        )
        
        req = self.build_request(
            method="POST",
            path="/chat/completions",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(request, False, False, "json", models.ChatCompletionRequest),
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = await self.do_request_async(
            hook_ctx=HookContext(operation_id="chat_completion_v1_chat_completions_post", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["422","4XX","5XX"],
            retry_config=retry_config
        )
        
        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(http_res.text, Optional[models.ChatCompletionResponse])
        if utils.match_response(http_res, "422", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.HTTPValidationErrorData)
            raise models.HTTPValidationError(data=data)
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
