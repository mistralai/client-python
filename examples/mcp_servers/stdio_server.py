import random
from mcp.server.fastmcp import FastMCP
import logging

logging.basicConfig(level=logging.ERROR)

# Initialize FastMCP server
mcp = FastMCP("weather")


@mcp.tool()
async def get_weather(location: str) -> float:
    return random.random() * 30


def run_stdio_server():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run_stdio_server()
