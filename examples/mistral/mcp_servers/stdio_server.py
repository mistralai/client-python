import random
from mcp.server.mcpserver import MCPServer
import logging

logging.basicConfig(level=logging.ERROR)

# Initialize MCP server
mcp = MCPServer("weather")


@mcp.tool()
async def get_weather(location: str) -> float:
    return random.random() * 30


def run_stdio_server():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run_stdio_server()
