"""Unit tests for the BatchJobs API (mistralai.client.batch_jobs.BatchJobs)."""

import json

import httpx
import pytest


# ---------------------------------------------------------------------------
# Mock response payloads
# ---------------------------------------------------------------------------

BATCH_JOB_RESPONSE = {
    "id": "batch-abc123",
    "object": "batch",
    "input_files": ["file-001"],
    "endpoint": "/v1/chat/completions",
    "model": "mistral-small-latest",
    "status": "QUEUED",
    "created_at": 1700000000,
    "total_requests": 10,
    "completed_requests": 0,
    "succeeded_requests": 0,
    "failed_requests": 0,
    "errors": [],
}

LIST_BATCH_JOBS_RESPONSE = {
    "data": [BATCH_JOB_RESPONSE],
    "object": "list",
    "total": 1,
}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestBatchJobsCreate:
    def test_create_returns_batch_job(self, mock_router, mistral_client):
        """batch_jobs.create() returns a BatchJob."""
        mock_router.post("/v1/batch/jobs").mock(
            return_value=httpx.Response(200, json=BATCH_JOB_RESPONSE)
        )
        result = mistral_client.batch.jobs.create(
            endpoint="/v1/chat/completions",
            input_files=["file-001"],
            model="mistral-small-latest",
        )
        assert result is not None
        assert result.id == "batch-abc123"
        assert result.status == "QUEUED"


class TestBatchJobsList:
    def test_list_returns_jobs(self, mock_router, mistral_client):
        """batch_jobs.list() returns a ListBatchJobsResponse."""
        mock_router.get("/v1/batch/jobs").mock(
            return_value=httpx.Response(200, json=LIST_BATCH_JOBS_RESPONSE)
        )
        result = mistral_client.batch.jobs.list()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].id == "batch-abc123"


class TestBatchJobsGet:
    def test_get_returns_job(self, mock_router, mistral_client):
        """batch_jobs.get(job_id=...) returns a BatchJob."""
        mock_router.get(url__regex=r"/v1/batch/jobs/[^/]+$").mock(
            return_value=httpx.Response(200, json=BATCH_JOB_RESPONSE)
        )
        result = mistral_client.batch.jobs.get(job_id="batch-abc123")
        assert result is not None
        assert result.id == "batch-abc123"


class TestBatchJobsCancel:
    def test_cancel_returns_job(self, mock_router, mistral_client):
        """batch_jobs.cancel(job_id=...) returns a BatchJob."""
        cancelled = {**BATCH_JOB_RESPONSE, "status": "CANCELLATION_REQUESTED"}
        mock_router.post(url__regex=r"/v1/batch/jobs/.*/cancel").mock(
            return_value=httpx.Response(200, json=cancelled)
        )
        result = mistral_client.batch.jobs.cancel(job_id="batch-abc123")
        assert result is not None
        assert result.status == "CANCELLATION_REQUESTED"


class TestBatchJobsListWithFilters:
    def test_list_with_filters(self, mock_router, mistral_client):
        """batch_jobs.list() passes query params for filtering."""
        mock_router.get("/v1/batch/jobs").mock(
            return_value=httpx.Response(200, json=LIST_BATCH_JOBS_RESPONSE)
        )
        result = mistral_client.batch.jobs.list(
            page=1,
            page_size=50,
            model="mistral-small-latest",
            created_by_me=True,
        )
        assert result is not None
        assert result.data is not None


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestBatchJobsCreateAsync:
    @pytest.mark.asyncio
    async def test_create_async(self, mock_router, mistral_client):
        """batch_jobs.create_async() returns a BatchJob."""
        mock_router.post("/v1/batch/jobs").mock(
            return_value=httpx.Response(200, json=BATCH_JOB_RESPONSE)
        )
        result = await mistral_client.batch.jobs.create_async(
            endpoint="/v1/chat/completions",
            input_files=["file-001"],
            model="mistral-small-latest",
        )
        assert result is not None
        assert result.id == "batch-abc123"


class TestBatchJobsGetAsync:
    @pytest.mark.asyncio
    async def test_get_async(self, mock_router, mistral_client):
        """batch_jobs.get_async(job_id=...) returns a BatchJob."""
        mock_router.get(url__regex=r"/v1/batch/jobs/[^/]+$").mock(
            return_value=httpx.Response(200, json=BATCH_JOB_RESPONSE)
        )
        result = await mistral_client.batch.jobs.get_async(job_id="batch-abc123")
        assert result is not None
        assert result.id == "batch-abc123"


class TestBatchJobsCancelAsync:
    @pytest.mark.asyncio
    async def test_cancel_async(self, mock_router, mistral_client):
        """batch_jobs.cancel_async(job_id=...) returns a BatchJob."""
        cancelled = {**BATCH_JOB_RESPONSE, "status": "CANCELLATION_REQUESTED"}
        mock_router.post(url__regex=r"/v1/batch/jobs/.*/cancel").mock(
            return_value=httpx.Response(200, json=cancelled)
        )
        result = await mistral_client.batch.jobs.cancel_async(job_id="batch-abc123")
        assert result is not None
        assert result.status == "CANCELLATION_REQUESTED"


class TestBatchJobsListAsync:
    @pytest.mark.asyncio
    async def test_list_async(self, mock_router, mistral_client):
        """batch_jobs.list_async() returns a ListBatchJobsResponse."""
        mock_router.get("/v1/batch/jobs").mock(
            return_value=httpx.Response(200, json=LIST_BATCH_JOBS_RESPONSE)
        )
        result = await mistral_client.batch.jobs.list_async()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].id == "batch-abc123"


class TestBatchJobsListPaginationParams:
    def test_list_sends_pagination_query_params(self, mock_router, mistral_client):
        """batch_jobs.list() serializes pagination params as query parameters."""
        route = mock_router.get("/v1/batch/jobs").mock(
            return_value=httpx.Response(200, json=LIST_BATCH_JOBS_RESPONSE)
        )
        mistral_client.batch.jobs.list(page=2, page_size=25)
        assert route.called
        request = route.calls.last.request
        assert "page=2" in str(request.url)
        assert "page_size=25" in str(request.url)
