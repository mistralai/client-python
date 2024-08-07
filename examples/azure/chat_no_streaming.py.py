import os

from mistralai_azure import MistralAzure

client = MistralAzure(
    azure_api_key=os.environ["AZURE_API_KEY"],
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
)

res = client.chat.complete(
    messages=[
        {"role": "user", "content": "What is the capital of France?"},
    ],
    # you don't need model as it will always be "azureai"
)
print(res.choices[0].message.content)
