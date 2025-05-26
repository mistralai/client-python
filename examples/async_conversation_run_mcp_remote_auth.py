#!/usr/bin/env python
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import threading
import webbrowser

from mistralai import Mistral
from mistralai.extra.run.context import RunContext

from mistralai.extra.mcp.sse import (
    MCPClientSSE,
    SSEServerParams,
)
from mistralai.extra.mcp.auth import build_oauth_params

MODEL = "mistral-medium-latest"

CALLBACK_PORT = 16010


# Use an official remote mcp server
# you can find some at:
# - https://mcpservers.org/remote-mcp-servers
# - https://support.anthropic.com/en/articles/11176164-pre-built-integrations-using-remote-mcp
# this one has auth: https://mcp.linear.app/sse


def run_callback_server(callback_func):
    auth_response: dict = {"url": ""}

    class OAuthCallbackHandler(BaseHTTPRequestHandler):
        server_version = "HTTP"
        code = None

        def do_GET(self):
            if "/callback" in self.path:
                try:
                    auth_response["url"] = self.path
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    callback_func()
                    response_html = "<html><body><p>You may now close this window.</p></body></html>"
                    self.wfile.write(response_html.encode())
                    threading.Thread(target=httpd.shutdown).start()
                except Exception:
                    self.send_response(500)
                    self.end_headers()

    server_address = ("localhost", CALLBACK_PORT)
    httpd = HTTPServer(server_address, OAuthCallbackHandler)
    threading.Thread(target=httpd.serve_forever).start()
    redirect_url = f"http://localhost:{CALLBACK_PORT}/oauth/callback"
    return httpd, redirect_url, auth_response


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    server_url = "https://mcp.linear.app/sse"

    # set-up the client
    mcp_client = MCPClientSSE(
        sse_params=SSEServerParams(
            url=server_url,
        )
    )

    callback_event = asyncio.Event()
    event_loop = asyncio.get_event_loop()

    # check if auth is required
    if await mcp_client.requires_auth():
        # let's login
        httpd, redirect_url, auth_response = run_callback_server(
            callback_func=lambda: event_loop.call_soon_threadsafe(callback_event.set)
        )
        try:
            # First create the required oauth config, this means fetching the server metadata and registering a client
            oauth_params = await build_oauth_params(
                mcp_client.base_url, redirect_url=redirect_url
            )
            mcp_client.set_oauth_params(oauth_params=oauth_params)
            login_url, state = await mcp_client.get_auth_url_and_state(redirect_url)

            # The oauth params like client_id, client_secret would generally be saved in some persistent storage.
            # The oauth state and token would be saved in a user session.

            # wait for the user to complete the authentication process
            print("Please go to this URL and authorize the application:", login_url)
            webbrowser.open(login_url, new=2)
            await callback_event.wait()

            # in a real app this would be your oauth2 callback route you would get the code from the query params,
            # verify the state, and then get the token
            # Here we recreate a new client with the saved params which and exchange the code for a token
            mcp_client = MCPClientSSE(
                sse_params=SSEServerParams(
                    url=server_url,
                ),
                oauth_params=oauth_params,
            )

            token = await mcp_client.get_token_from_auth_response(
                auth_response["url"], redirect_url=redirect_url, state=state
            )
            mcp_client.set_auth_token(token)

        except Exception as e:
            print(f"Error during authentication: {e}")
        finally:
            httpd.shutdown()
            httpd.server_close()

    # Now it's possible to make a query to the mcp server as we would do without authentication
    async with RunContext(
        model=MODEL,
    ) as run_ctx:
        # Add mcp client to the run context
        await run_ctx.register_mcp_client(mcp_client=mcp_client)

        run_result = await client.beta.conversations.run_async(
            run_ctx=run_ctx,
            inputs="Tell me which projects do I have in my workspace?",
        )

        print(f"Final Response: {run_result.output_as_text}")


if __name__ == "__main__":
    asyncio.run(main())
