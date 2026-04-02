#!/usr/bin/env python

import asyncio
import os

from mistralai.client import Mistral
from mistralai.extra.workflows.helpers import get_scheduler_namespace


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)
    print(await get_scheduler_namespace(client))


if __name__ == "__main__":
    asyncio.run(main())
