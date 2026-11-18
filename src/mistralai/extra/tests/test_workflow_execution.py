import json

import httpx2 as httpx
import pytest

from mistralai.client import Mistral


@pytest.mark.asyncio
@pytest.mark.parametrize("is_async", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("use_api_sync", [False, True], ids=["poll", "wait"])
async def test_execute_and_wait_routes_through_deployment_name(
    is_async: bool, use_api_sync: bool
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert (request.method, request.url.path) in {
            ("POST", "/v1/workflows/root-wf/execute"),
            ("GET", "/v1/workflows/executions/root-exec"),
        }
        return httpx.Response(
            200,
            json={
                "workflow_name": "root-wf",
                "execution_id": "root-exec",
                "root_execution_id": "root-exec",
                "status": "COMPLETED",
                "start_time": "2026-01-01T00:00:00Z",
                "end_time": "2026-01-01T00:00:01Z",
                "result": {"answer": 42},
            },
        )

    with httpx.Client(transport=httpx.MockTransport(handle)) as http_client:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handle)
        ) as async_client:
            client = Mistral(
                api_key="test-api-key",
                server_url="https://api.example.test",
                client=http_client,
                async_client=async_client,
            )
            if is_async:
                result = await client.workflows.execute_workflow_and_wait_async(
                    workflow_identifier="root-wf",
                    deployment_name="test-deployment",
                    use_api_sync=use_api_sync,
                    polling_interval=0,
                    max_attempts=1,
                )
            else:
                result = client.workflows.execute_workflow_and_wait(
                    workflow_identifier="root-wf",
                    deployment_name="test-deployment",
                    use_api_sync=use_api_sync,
                    polling_interval=0,
                    max_attempts=1,
                )

    assert result == {"answer": 42}
    assert len(requests) == (1 if use_api_sync else 2)
    assert requests[0].method == "POST"
    body = json.loads(requests[0].content)
    assert body["deployment_name"] == "test-deployment"
    assert "task_queue" not in body
    assert body.get("wait_for_result", False) is use_api_sync
