import os
from mistralai.client import Mistral

from mistralai.extra.run.context import RunContext
import logging
import time
import asyncio


MODEL = "mistral-medium-latest"

USER_MESSAGE = """
Please make the Secret Santa for me
To properly do it you need to:
- Get the friend you were assigned to (using the get_secret_santa_assignment function)
- Read into his gift wishlist what they would like to receive (using the get_gift_wishlist function)
- Buy the gift (using the buy_gift function)
- Find the best website to buy the gift using a web search
- Send it to them (using the send_gift function)
"""


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    mistral_agent_id = os.environ["MISTRAL_AGENT_ID"]
    client = Mistral(
        api_key=api_key, debug_logger=logging.getLogger("mistralai")
    )

    async with RunContext(
        agent_id=mistral_agent_id
    ) as run_context:
        run_context.register_func(get_secret_santa_assignment)
        run_context.register_func(get_gift_wishlist)
        run_context.register_func(buy_gift)
        run_context.register_func(send_gift)

        await client.beta.conversations.run_async(
            run_ctx=run_context,
            inputs=USER_MESSAGE,
        )


def get_secret_santa_assignment():
    """Get the friend you were assigned to"""
    time.sleep(2)
    return "John Doe"


def get_gift_wishlist(friend_name: str):
    """Get the gift wishlist of the friend you were assigned to"""
    time.sleep(1.5)
    return ["Book", "Chocolate", "T-Shirt"]


def buy_gift(gift_name: str):
    """Buy the gift you want to send to your friend"""
    time.sleep(1.1)
    return f"Bought {gift_name}"


def send_gift(friend_name: str, gift_name: str, website: str):
    """Send the gift to your friend"""
    time.sleep(2.2)
    return f"Sent {gift_name} to {friend_name} bought on {website}"


if __name__ == "__main__":
    asyncio.run(main())