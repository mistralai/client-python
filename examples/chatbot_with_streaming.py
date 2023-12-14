#!/usr/bin/env python

# Simple chatbot example -- run with -h argument to see options.

import argparse
import logging
import os
import sys

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

MODEL_LIST = [
    "mistral-tiny",
    "mistral-small",
    "mistral-medium",
]
DEFAULT_MODEL = "mistral-small"

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

logger = logging.getLogger("chatbot")


class ChatBot:
    def __init__(self, api_key, model, temperature, system_message=None):
        self.client = MistralClient(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.system_message = system_message

    def opening_instructions(self):
        print(
            """
To chat: type your message and hit enter
To start a new chat: type /new
To exit: type /exit, /quit, or hit CTRL+C
"""
        )

    def new_chat(self):
        self.messages = []
        if self.system_message:
            self.messages.append(
                ChatMessage(role="system", content=self.system_message)
            )

    def check_exit(self, content):
        if content.lower().strip() in ["/exit", "/quit"]:
            self.exit()

    def check_new_chat(self, content):
        if content.lower().strip() in ["/new"]:
            print("")
            print("Starting new chat...")
            print("")
            self.new_chat()
            return True
        return False

    def run_inference(self, content):
        self.messages.append(ChatMessage(role="user", content=content))

        assistant_response = ""
        logger.debug(f"Sending messages: {self.messages}")
        for chunk in self.client.chat_stream(model=self.model, messages=self.messages):
            response = chunk.choices[0].delta.content
            if response is not None:
                print(response, end="", flush=True)
                assistant_response += response

        print("", flush=True)

        if assistant_response:
            self.messages.append(
                ChatMessage(role="assistant", content=assistant_response)
            )
        logger.debug(f"Current messages: {self.messages}")

    def start(self):
        self.opening_instructions()
        self.new_chat()
        while True:
            try:
                content = input(f"\033[38;2;50;168;82mUser: \033[0m")
                self.check_exit(content)
                if not self.check_new_chat(content):
                    print(f"\033[38;2;253;112;0m{self.model}: \033[0m", end="")
                    self.run_inference(content)

            except KeyboardInterrupt:
                self.exit()

    def exit(self):
        logger.debug("Exiting chatbot")
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple chatbot using the Mistral API"
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("MISTRAL_API_KEY"),
        help="Mistral API key. Defaults to environment variable MISTRAL_API_KEY",
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=MODEL_LIST,
        default=DEFAULT_MODEL,
        help="Model for chat inference. Choices are %(choices)s. Defaults to %(default)s",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        default=0.7,
        help="Temperature of the model. Defaults to 0.7.",
    )
    parser.add_argument(
        "-s", "--system-message", help="Optional system message to prepend."
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logging"
    )

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

    bot = ChatBot(args.api_key, args.model, args.temperature, args.system_message)
    bot.start()
