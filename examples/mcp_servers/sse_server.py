import random
import threading
from contextlib import contextmanager

from mcp.server.fastmcp import FastMCP
import logging

logging.basicConfig(level=logging.ERROR)

# Initialize FastMCP server
mcp = FastMCP("weather")


@mcp.tool()
async def get_weather(location: str) -> float:
    return random.random() * 30


def run_sse_server():
    mcp.run(transport="sse")


@contextmanager
def run_sse_server_in_background():
    """start the server in a new thread"""
    thread = threading.Thread(target=run_sse_server, daemon=True)
    thread.start()
    yield thread


if __name__ == "__main__":
    run_sse_server()
