#!/usr/bin/env python

import os

from mistralai.client import Mistral
from mistralai.client.models import UserMessage


def main():

    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    code = """class Cheese(BaseModel):
    name: str
    type: str
    country_of_origin: str

my_cheese = Cheese(name="Brie", type="Soft", country_of_origin="France")
"""
    refactor_prompt = 'Add a "price" property of type float to the Cheese class. Respond only with code, no explanation, no formatting.'

    chat_response = client.chat.complete(
        model="codestral-latest",
        messages=[
            UserMessage(content=refactor_prompt),
            UserMessage(content=code)
        ],
        prediction= {
            "type": "content",
            "content": refactor_prompt,
        }
    )
    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
