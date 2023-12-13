#!/usr/bin/env python

# Simple chatbot example -- run with -h argument to see options.

import os
import sys
import argparse
import logging

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

MODEL_LIST = [
    "mistral-tiny",
    "mistral-small",
    "mistral-medium",
]
DEFAULT_MODEL = "mistral-small"

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

logger = logging.getLogger('chatbot')


class ChatBot:
    def __init__(self, api_key, model, system_message=None):
        self.client = MistralClient(api_key=api_key)
        self.model = model
        self.system_message = system_message

    def start(self):
        messages = []
        if self.system_message:
            messages.append(ChatMessage(role="system", content=self.system_message))

        print("")
        print("To chat, type your message and hit enter. To exit, type 'exit', 'quit', or hit CTRL+C.")

        while True:
            try:
                print("")
                content = input("YOU: ")
                if content.lower().strip() in ["exit", "quit"]:
                    self.exit()

                print("")
                print("MISTRAL:")
                print("")

                messages.append(ChatMessage(role="user", content=content))

                assistant_response = ""
                logger.debug(f"Sending messages: {messages}")
                for chunk in self.client.chat_stream(model=self.model, messages=messages):
                    response = chunk.choices[0].delta.content
                    if response is not None:
                        print(response, end="", flush=True)
                        assistant_response += response

                print("", flush=True)

                if assistant_response:
                    messages.append(ChatMessage(role="assistant", content=assistant_response))
                logger.debug(f"Current messages: {messages}")
            except KeyboardInterrupt:
                self.exit()

    def exit(self):
        logger.debug("Exiting chatbot")
        sys.exit(0)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A simple chatbot using the Mistral API")
    parser.add_argument("--api-key", default=os.environ.get("MISTRAL_API_KEY"),
                        help="Mistral API key. Defaults to environment variable MISTRAL_API_KEY")
    parser.add_argument("-m", "--model", choices=MODEL_LIST,
                        default=DEFAULT_MODEL,
                        help="Model for chat inference. Choices are %(choices)s. Defaults to %(default)s")
    parser.add_argument("-s", "--system-message",
                        help="Optional system message to prepend.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    formatter = logging.Formatter(LOG_FORMAT)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.debug(f"Starting chatbot with model: {args.model}")

    bot = ChatBot(args.api_key, args.model, args.system_message)
    bot.start()
