import json
import os
import time
from typing import Optional, Type

from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from pydantic import BaseModel, ConfigDict, ValidationError

load_dotenv()


class MistralLanguageModel:
    def __init__(
        self,
        api_key=os.environ["MISTRAL_API_KEY"],
        model="mistral-tiny",
        temperature=0.5,
    ):
        if api_key is None:
            raise ValueError(
                "The Mistral API KEY must be provided either as "
                "an argument or as an environment variable "
                "named 'MISTRAL_API_KEY'"
            )

        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.client = MistralClient(api_key=self.api_key)

    def generate(
        self,
        prompt: str,
        output_format: Optional[Type[BaseModel]] = None,
        max_tokens: int = None,
    ):
        retry_delay = 0.1

        while True:
            try:
                system_message = "You are a helpful assistant."
                if output_format:
                    system_message += f" Respond in a JSON format that contains the following keys: {self._model_structure_repr(output_format)}"  # noqa

                messages = [
                    ChatMessage(role="system", content=system_message),
                    ChatMessage(role="user", content=prompt),
                ]
                params = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": self.temperature,
                }

                if max_tokens is not None:
                    params["max_tokens"] = max_tokens

                response = self.client.chat(**params)
                response_content = response.choices[0].message.content

                if output_format:
                    if self._is_valid_json_for_model(response_content,
                                                     output_format):
                        return response_content
                else:
                    return response_content

            except Exception as e:
                print(f"Hit rate limit. Retrying in {retry_delay} seconds.")
                print(f"Error: {e}")
                time.sleep(retry_delay)
                retry_delay *= 2

    def _model_structure_repr(self, model: Type[BaseModel]) -> str:
        fields = model.__annotations__
        return ", ".join(f"{key}: {value}" for key, value in fields.items())

    def _is_valid_json_for_model(self, text: str, model: Type[BaseModel]) -> bool:  # noqa
        """
        Check if a text is valid JSON and if it respects the provided BaseModel. # noqa
        """
        model.model_config = ConfigDict(strict=True)

        try:
            parsed_data = json.loads(text)
            model(**parsed_data)
            return True
        except (json.JSONDecodeError, ValidationError):
            return False


class Output(BaseModel):
    first_name: str
    last_name: str
    city: str

# This works well for mistral-tiny and mistral-small.

llm = MistralLanguageModel()
prompt = 'Extract the requested  information from the following sentence: "Alice Johnson is visiting Rome."' # noqa
response = llm.generate(prompt, output_format=Output)

print(response)
