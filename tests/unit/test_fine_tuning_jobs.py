"""Unit tests for the FineTuningJobs API (mistralai.client.fine_tuning_jobs.FineTuningJobs)."""

import json

import httpx
import pytest


# ---------------------------------------------------------------------------
# Mock response payloads
# ---------------------------------------------------------------------------

FT_JOB_RESPONSE = {
    "id": "ftjob-abc123",
    "object": "job",
    "model": "open-mistral-7b",
    "status": "QUEUED",
    "job_type": "completion",
    "created_at": 1700000000,
    "modified_at": 1700000000,
    "auto_start": True,
    "training_files": ["file-001"],
    "hyperparameters": {
        "training_steps": 10,
        "learning_rate": 0.0001,
    },
}

LIST_FT_JOBS_RESPONSE = {
    "data": [FT_JOB_RESPONSE],
    "object": "list",
    "total": 1,
}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestFineTuningJobsCreate:
    def test_create_returns_job(self, mock_router, mistral_client):
        """fine_tuning.jobs.create() returns a fine-tuning job response."""
        mock_router.post("/v1/fine_tuning/jobs").mock(
            return_value=httpx.Response(200, json=FT_JOB_RESPONSE)
        )
        result = mistral_client.fine_tuning.jobs.create(
            model="open-mistral-7b",
            hyperparameters={"training_steps": 10, "learning_rate": 0.0001},
            training_files=[
                {"file_id": "file-001", "weight": 1},
            ],
        )
        assert result is not None
        assert result.id == "ftjob-abc123"
        assert result.status == "QUEUED"


class TestFineTuningJobsList:
    def test_list_returns_jobs(self, mock_router, mistral_client):
        """fine_tuning.jobs.list() returns a ListFineTuningJobsResponse."""
        mock_router.get("/v1/fine_tuning/jobs").mock(
            return_value=httpx.Response(200, json=LIST_FT_JOBS_RESPONSE)
        )
        result = mistral_client.fine_tuning.jobs.list()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].id == "ftjob-abc123"


class TestFineTuningJobsGet:
    def test_get_returns_job(self, mock_router, mistral_client):
        """fine_tuning.jobs.get(job_id=...) returns a fine-tuning job."""
        mock_router.get(url__regex=r"/v1/fine_tuning/jobs/[^/]+$").mock(
            return_value=httpx.Response(200, json=FT_JOB_RESPONSE)
        )
        result = mistral_client.fine_tuning.jobs.get(job_id="ftjob-abc123")
        assert result is not None
        assert result.id == "ftjob-abc123"


class TestFineTuningJobsCancel:
    def test_cancel_returns_job(self, mock_router, mistral_client):
        """fine_tuning.jobs.cancel(job_id=...) cancels a job."""
        cancelled = {**FT_JOB_RESPONSE, "status": "CANCELLED"}
        mock_router.post(url__regex=r"/v1/fine_tuning/jobs/.*/cancel").mock(
            return_value=httpx.Response(200, json=cancelled)
        )
        result = mistral_client.fine_tuning.jobs.cancel(job_id="ftjob-abc123")
        assert result is not None
        assert result.status == "CANCELLED"


class TestFineTuningJobsStart:
    def test_start_returns_job(self, mock_router, mistral_client):
        """fine_tuning.jobs.start(job_id=...) starts a validated job."""
        started = {**FT_JOB_RESPONSE, "status": "STARTED"}
        mock_router.post(url__regex=r"/v1/fine_tuning/jobs/.*/start").mock(
            return_value=httpx.Response(200, json=started)
        )
        result = mistral_client.fine_tuning.jobs.start(job_id="ftjob-abc123")
        assert result is not None
        assert result.status == "STARTED"


class TestFineTuningJobsCreateRequestBody:
    def test_create_request_body(self, mock_router, mistral_client):
        """fine_tuning.jobs.create() sends model, training_files, hyperparameters."""
        mock_router.post("/v1/fine_tuning/jobs").mock(
            return_value=httpx.Response(200, json=FT_JOB_RESPONSE)
        )
        result = mistral_client.fine_tuning.jobs.create(
            model="open-mistral-7b",
            hyperparameters={"training_steps": 20, "learning_rate": 0.0002},
            training_files=[
                {"file_id": "file-001", "weight": 1},
            ],
        )
        assert result is not None
        # Verify the request body contains expected fields
        req_body = json.loads(mock_router.calls.last.request.content)
        assert req_body["model"] == "open-mistral-7b"
        assert "hyperparameters" in req_body
        assert req_body["hyperparameters"]["training_steps"] == 20


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestFineTuningJobsCreateAsync:
    @pytest.mark.asyncio
    async def test_create_async(self, mock_router, mistral_client):
        """fine_tuning.jobs.create_async() returns a fine-tuning job response."""
        mock_router.post("/v1/fine_tuning/jobs").mock(
            return_value=httpx.Response(200, json=FT_JOB_RESPONSE)
        )
        result = await mistral_client.fine_tuning.jobs.create_async(
            model="open-mistral-7b",
            hyperparameters={"training_steps": 10, "learning_rate": 0.0001},
            training_files=[
                {"file_id": "file-001", "weight": 1},
            ],
        )
        assert result is not None
        assert result.id == "ftjob-abc123"


class TestFineTuningJobsListAsync:
    @pytest.mark.asyncio
    async def test_list_async(self, mock_router, mistral_client):
        """fine_tuning.jobs.list_async() returns a ListFineTuningJobsResponse."""
        mock_router.get("/v1/fine_tuning/jobs").mock(
            return_value=httpx.Response(200, json=LIST_FT_JOBS_RESPONSE)
        )
        result = await mistral_client.fine_tuning.jobs.list_async()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1


class TestFineTuningJobsGetAsync:
    @pytest.mark.asyncio
    async def test_get_async(self, mock_router, mistral_client):
        """fine_tuning.jobs.get_async(job_id=...) returns a fine-tuning job."""
        mock_router.get(url__regex=r"/v1/fine_tuning/jobs/[^/]+$").mock(
            return_value=httpx.Response(200, json=FT_JOB_RESPONSE)
        )
        result = await mistral_client.fine_tuning.jobs.get_async(
            job_id="ftjob-abc123"
        )
        assert result is not None
        assert result.id == "ftjob-abc123"


class TestFineTuningJobsCancelAsync:
    @pytest.mark.asyncio
    async def test_cancel_async(self, mock_router, mistral_client):
        """fine_tuning.jobs.cancel_async(job_id=...) cancels a job."""
        cancelled = {**FT_JOB_RESPONSE, "status": "CANCELLED"}
        mock_router.post(url__regex=r"/v1/fine_tuning/jobs/.*/cancel").mock(
            return_value=httpx.Response(200, json=cancelled)
        )
        result = await mistral_client.fine_tuning.jobs.cancel_async(
            job_id="ftjob-abc123"
        )
        assert result is not None
        assert result.status == "CANCELLED"


class TestFineTuningJobsStartAsync:
    @pytest.mark.asyncio
    async def test_start_async(self, mock_router, mistral_client):
        """fine_tuning.jobs.start_async(job_id=...) starts a validated job."""
        started = {**FT_JOB_RESPONSE, "status": "STARTED"}
        mock_router.post(url__regex=r"/v1/fine_tuning/jobs/.*/start").mock(
            return_value=httpx.Response(200, json=started)
        )
        result = await mistral_client.fine_tuning.jobs.start_async(
            job_id="ftjob-abc123"
        )
        assert result is not None
        assert result.status == "STARTED"
