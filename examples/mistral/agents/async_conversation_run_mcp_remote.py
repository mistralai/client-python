#!/usr/bin/env python
import asyncio
import os

from mistralai import Mistral
from mistralai.extra.run.context import RunContext

from mistralai.extra.mcp.sse import (
    MCPClientSSE,
    SSEServerParams,
)
from pathlib import Path

cwd = Path(__file__).parent
MODEL = "mistral-medium-latest"

# Use an official remote mcp server
# you can find some at:
# - https://mcpservers.org/remote-mcp-servers
# this one does not require auth: https://remote.mcpservers.org/edgeone-pages/mcp


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    server_url = "https://mcp.semgrep.ai/sse"
    mcp_client = MCPClientSSE(sse_params=SSEServerParams(url=server_url, timeout=100))

    async with RunContext(
        model=MODEL,
    ) as run_ctx:
        # Add mcp client to the run context
        await run_ctx.register_mcp_client(mcp_client=mcp_client)

        run_result = await client.beta.conversations.run_async(
            run_ctx=run_ctx,
            inputs="Can you write a hello_world.py and check for security vulnerabilities",
        )

        print("All run entries:")
        for entry in run_result.output_entries:
            print(f"{entry}")
            print()
        print(f"Final Response: {run_result.output_as_text}")


if __name__ == "__main__":
    asyncio.run(main())
