from typing import Optional
import logging
from contextlib import AsyncExitStack

from mistralai.extra.mcp.base import (
    MCPClientBase,
)

from mcp import stdio_client, StdioServerParameters

logger = logging.getLogger(__name__)


class MCPClientSTDIO(MCPClientBase):
    """MCP client that uses stdio for communication."""

    def __init__(self, stdio_params: StdioServerParameters, name: Optional[str] = None):
        super().__init__(name=name)
        self._stdio_params = stdio_params

    async def _get_transport(self, exit_stack: AsyncExitStack):
        return await exit_stack.enter_async_context(stdio_client(self._stdio_params))
