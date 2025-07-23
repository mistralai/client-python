#!/usr/bin/env python

import os

from mistralai import Mistral


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    list_models_response = client.models.list()
    print(list_models_response)


if __name__ == "__main__":
    main()
