import os

from mistralai.azure.client import MistralAzure
from mistralai.azure.client.models import ChatCompletionRequestMessage, UserMessage

client = MistralAzure(
    api_key=os.environ["AZURE_API_KEY"],
    server_url=os.environ["AZURE_ENDPOINT"],
)

messages: list[ChatCompletionRequestMessage] = [
    UserMessage(content="What is the capital of France?"),
]
res = client.chat.complete(messages=messages)
print(res.choices[0].message.content)
