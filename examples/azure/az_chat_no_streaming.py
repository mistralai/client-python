import os

from mistralai_azure import MistralAzure
from mistralai_azure.models import ChatCompletionRequestMessages, UserMessage

client = MistralAzure(
    azure_api_key=os.environ["AZURE_API_KEY"],
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
)

messages: list[ChatCompletionRequestMessages] = [
    UserMessage(content="What is the capital of France?"),
]
res = client.chat.complete(messages=messages)
print(res.choices[0].message.content)
