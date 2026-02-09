#!/usr/bin/env python
import asyncio
import os
import random

from mistralai.client import Mistral
from mistralai.extra.run.context import RunContext
from mcp import StdioServerParameters
from mistralai.extra.mcp.stdio import MCPClientSTDIO
from pathlib import Path

from mistralai.extra.run.result import RunResult
from mistralai.client.types import BaseModel

cwd = Path(__file__).parent
MODEL = "mistral-medium-latest"


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    # Create a mcp server has a tool to return the weather based on the location
    server_params = StdioServerParameters(
        command="python",
        args=[str((cwd / "mcp_servers/stdio_server.py").resolve())],
        env=None,
    )

    weather_agent = client.beta.agents.create(
        model=MODEL,
        name="weather teller",
        instructions="You are able to tell the weather.",
        description="",
    )

    class WeatherResult(BaseModel):
        user: str
        location: str
        temperature: float

    async with RunContext(
        agent_id=weather_agent.id,
        output_format=WeatherResult,
    ) as run_ctx:
        # Add location function to the run context
        @run_ctx.register_func
        def get_location(name: str) -> str:
            """function to get location of a user.

            Args:
                name: name of the user.
            """
            return random.choice(["New York", "London", "Paris", "Tokyo", "Sydney"])

        # Add mcp client to the run context
        mcp_client = MCPClientSTDIO(stdio_params=server_params)
        await run_ctx.register_mcp_client(mcp_client=mcp_client)

        events = await client.beta.conversations.run_stream_async(
            run_ctx=run_ctx,
            inputs="Tell me the weather in John's location currently.",
        )

        run_result = None
        async for event in events:
            if isinstance(event, RunResult):
                run_result = event
            else:
                print(event)

        if not run_result:
            raise RuntimeError("not run result found")

        print("All run entries:")
        for entry in run_result.output_entries:
            print(f"{entry}")
        print(f"Final model: {run_result.output_as_model}")


if __name__ == "__main__":
    asyncio.run(main())
