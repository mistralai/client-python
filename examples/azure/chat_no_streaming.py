import os

from mistralai.azure.client import MistralAzure
from mistralai.azure.client.models import ChatCompletionRequestMessage, UserMessage

AZURE_API_KEY = os.environ["AZURE_API_KEY"]
AZURE_ENDPOINT = os.environ["AZURE_ENDPOINT"]
AZURE_MODEL = os.environ["AZURE_MODEL"]
AZURE_API_VERSION = os.environ.get("AZURE_API_VERSION", "2024-05-01-preview")

# The SDK automatically injects api-version as a query parameter
client = MistralAzure(
    api_key=AZURE_API_KEY,
    server_url=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION,
)

messages: list[ChatCompletionRequestMessage] = [
    UserMessage(content="What is the capital of France?"),
]
res = client.chat.complete(model=AZURE_MODEL, messages=messages)
print(res.choices[0].message.content)
