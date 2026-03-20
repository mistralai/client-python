import functools
import json
import os
from typing import Any

from mistralai.client import Mistral
from mistralai.client.models import (
    AssistantMessage,
    ChatCompletionRequestMessage,
    Function,
    Tool,
    ToolMessage,
    UserMessage,
)

# Assuming we have the following data
data: dict[str, list[Any]] = {
    "transaction_id": ["T1001", "T1002", "T1003", "T1004", "T1005"],
    "customer_id": ["C001", "C002", "C003", "C002", "C001"],
    "payment_amount": [125.50, 89.99, 120.00, 54.30, 210.20],
    "payment_date": [
        "2021-10-05",
        "2021-10-06",
        "2021-10-07",
        "2021-10-05",
        "2021-10-08",
    ],
    "payment_status": ["Paid", "Unpaid", "Paid", "Paid", "Pending"],
}


def retrieve_payment_status(data: dict[str, list[Any]], transaction_id: str) -> str:
    for i, r in enumerate(data["transaction_id"]):
        if r == transaction_id:
            return json.dumps({"status": data["payment_status"][i]})
    return json.dumps({"status": "Error - transaction id not found"})


def retrieve_payment_date(data: dict[str, list[Any]], transaction_id: str) -> str:
    for i, r in enumerate(data["transaction_id"]):
        if r == transaction_id:
            return json.dumps({"date": data["payment_date"][i]})
    return json.dumps({"status": "Error - transaction id not found"})


names_to_functions = {
    "retrieve_payment_status": functools.partial(retrieve_payment_status, data=data),
    "retrieve_payment_date": functools.partial(retrieve_payment_date, data=data),
}

tools: list[Tool] = [
    Tool(
        function=Function(
            name="retrieve_payment_status",
            description="Get payment status of a transaction id",
            parameters={
                "type": "object",
                "required": ["transaction_id"],
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "The transaction id.",
                    }
                },
            },
        ),
    ),
    Tool(
        function=Function(
            name="retrieve_payment_date",
            description="Get payment date of a transaction id",
            parameters={
                "type": "object",
                "required": ["transaction_id"],
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "The transaction id.",
                    }
                },
            },
        ),
    ),
]

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-small-latest"

client = Mistral(api_key=api_key)

messages: list[ChatCompletionRequestMessage] = [
    UserMessage(content="What's the status of my transaction?")
]

response = client.chat.complete(model=model, messages=messages, tools=tools, temperature=0)

print(response.choices[0].message.content)

messages.append(AssistantMessage(content=response.choices[0].message.content))
messages.append(UserMessage(content="My transaction ID is T1001."))

response = client.chat.complete(model=model, messages=messages, tools=tools, temperature=0)

tool_calls = response.choices[0].message.tool_calls
if not tool_calls:
    raise RuntimeError("Expected tool calls")
tool_call = tool_calls[0]
function_name = tool_call.function.name
function_params = json.loads(str(tool_call.function.arguments))

print(f"calling function_name: {function_name}, with function_params: {function_params}")

function_result = names_to_functions[function_name](**function_params)

messages.append(
    AssistantMessage(
        content=response.choices[0].message.content,
        tool_calls=response.choices[0].message.tool_calls,
    )
)
messages.append(
    ToolMessage(
        name=function_name,
        content=function_result,
        tool_call_id=tool_call.id,
    )
)
print(messages)

response = client.chat.complete(model=model, messages=messages, tools=tools, temperature=0)

print(f"{response.choices[0].message.content}")
