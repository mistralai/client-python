#!/usr/bin/env python

# Simple chatbot example -- run with -h argument to see options.

import argparse
import logging
import os
import readline
import sys

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

MODEL_LIST = [
    "mistral-tiny",
    "mistral-small",
    "mistral-medium",
]
DEFAULT_MODEL = "mistral-small"
DEFAULT_TEMPERATURE = 0.7
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# A dictionary of all commands and their arguments, used for tab completion.
COMMAND_LIST = {
    "/new": {},
    "/help": {},
    "/model": {model: {} for model in MODEL_LIST},  # Nested completions for models
    "/system": {},
    "/temperature": {},
    "/config": {},
    "/quit": {},
    "/exit": {},
}

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

logger = logging.getLogger("chatbot")


def find_completions(command_dict, parts):
    if not parts:
        return command_dict.keys()
    if parts[0] in command_dict:
        return find_completions(command_dict[parts[0]], parts[1:])
    else:
        return [cmd for cmd in command_dict if cmd.startswith(parts[0])]


def completer(text, state):
    buffer = readline.get_line_buffer()
    line_parts = buffer.lstrip().split(' ')
    options = find_completions(COMMAND_LIST, line_parts[:-1])

    try:
        return [option for option in options if option.startswith(line_parts[-1])][state]
    except IndexError:
        return None


readline.set_completer(completer)
readline.set_completer_delims(" ")
# Enable tab completion
readline.parse_and_bind("tab: complete")


class ChatBot:
    def __init__(
        self, api_key, model, system_message=None, temperature=DEFAULT_TEMPERATURE
    ):
        self.client = MistralClient(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.system_message = system_message

    def opening_instructions(self):
        print(
            """
To chat: type your message and hit enter
To start a new chat: /new
To switch model: /model <model name>
To switch system message: /system <message>
To switch temperature: /temperature <temperature>
To see current config: /config
To exit: /exit, /quit, or hit CTRL+C
To see this help: /help
"""
        )

    def new_chat(self):
        print("")
        print(
            f"Starting new chat with model: {self.model}, temperature: {self.temperature}"
        )
        print("")
        self.messages = []
        if self.system_message:
            self.messages.append(
                ChatMessage(role="system", content=self.system_message)
            )

    def switch_model(self, input):
        model = self.get_arguments(input)
        if model in MODEL_LIST:
            self.model = model
            logger.info(f"Switching model: {model}")
        else:
            logger.error(f"Invalid model name: {model}")

    def switch_system_message(self, input):
        system_message = self.get_arguments(input)
        if system_message:
            self.system_message = system_message
            logger.info(f"Switching system message: {system_message}")
            self.new_chat()
        else:
            logger.error(f"Invalid system message: {system_message}")

    def switch_temperature(self, input):
        temperature = self.get_arguments(input)
        try:
            temperature = float(temperature)
            if temperature < 0 or temperature > 1:
                raise ValueError
            self.temperature = temperature
            logger.info(f"Switching temperature: {temperature}")
        except ValueError:
            logger.error(f"Invalid temperature: {temperature}")

    def show_config(self):
        print("")
        print(f"Current model: {self.model}")
        print(f"Current temperature: {self.temperature}")
        print(f"Current system message: {self.system_message}")
        print("")

    def collect_user_input(self):
        print("")
        return input("YOU: ")

    def run_inference(self, content):
        print("")
        print("MISTRAL:")
        print("")

        self.messages.append(ChatMessage(role="user", content=content))

        assistant_response = ""
        logger.debug(
            f"Running inference with model: {self.model}, temperature: {self.temperature}"
        )
        logger.debug(f"Sending messages: {self.messages}")
        for chunk in self.client.chat_stream(
            model=self.model, temperature=self.temperature, messages=self.messages
        ):
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

    def get_command(self, input):
        return input.split()[0].strip()

    def get_arguments(self, input):
        try:
            return " ".join(input.split()[1:])
        except IndexError:
            return ""

    def is_command(self, input):
        return self.get_command(input) in COMMAND_LIST

    def execute_command(self, input):
        command = self.get_command(input)
        if command in ["/exit", "/quit"]:
            self.exit()
        elif command == "/help":
            self.opening_instructions()
        elif command == "/new":
            self.new_chat()
        elif command == "/model":
            self.switch_model(input)
        elif command == "/system":
            self.switch_system_message(input)
        elif command == "/temperature":
            self.switch_temperature(input)
        elif command == "/config":
            self.show_config()

    def start(self):
        self.opening_instructions()
        self.new_chat()
        while True:
            try:
                input = self.collect_user_input()
                if self.is_command(input):
                    self.execute_command(input)
                else:
                    self.run_inference(input)

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
        "-s", "--system-message", help="Optional system message to prepend."
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help="Optional temperature for chat inference. Defaults to %(default)s",
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

    logger.debug(
        f"Starting chatbot with model: {args.model}, "
        f"temperature: {args.temperature}, "
        f"system message: {args.system_message}"
    )

    bot = ChatBot(args.api_key, args.model, args.system_message, args.temperature)
    bot.start()
