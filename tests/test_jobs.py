import orjson
from mistralai.models.jobs import DetailedJob, Job, TrainingParameters

from .utils import (
    mock_detailed_job_response_payload,
    mock_job_response_payload,
    mock_response,
)


class TestJobsClient:
    def test_create(self, client):
        expected_response_job = Job.model_validate_json(mock_job_response_payload())
        client._client.request.return_value = mock_response(
            200,
            expected_response_job.model_dump_json(),
        )

        response_job = client.jobs.create(
            model="model",
            training_files=["training_file_id"],
            validation_files=["validation_file_id"],
            hyperparameters=TrainingParameters(
                training_steps=1800,
                learning_rate=1.0e-4,
            ),
        )

        client._client.request.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/fine_tuning/jobs",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={
                "model": "model",
                "training_files": ["training_file_id"],
                "validation_files": ["validation_file_id"],
                "hyperparameters": {
                    "training_steps": 1800,
                    "learning_rate": 1.0e-4,
                },
                "suffix": None,
                "integrations": None,
            },
            data=None,
            params={"dry_run": False},
        )
        assert response_job == expected_response_job

    def test_retrieve(self, client):
        expected_response_job = DetailedJob.model_validate_json(mock_detailed_job_response_payload())
        client._client.request.return_value = mock_response(
            200,
            expected_response_job.model_dump_json(),
        )

        response_job = client.jobs.retrieve("job_id")

        client._client.request.assert_called_once_with(
            "get",
            "https://api.mistral.ai/v1/fine_tuning/jobs/job_id",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
        )
        assert response_job == expected_response_job

    def test_list(self, client):
        expected_response_job = Job.model_validate_json(mock_job_response_payload())
        client._client.request.return_value = mock_response(
            200,
            orjson.dumps(
                {
                    "data": [expected_response_job.model_dump()],
                    "object": "list",
                }
            ),
        )

        response_jobs = client.jobs.list()
        response_job = response_jobs.data[0]

        client._client.request.assert_called_once_with(
            "get",
            "https://api.mistral.ai/v1/fine_tuning/jobs",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
            params={"page": 0, "page_size": 10},
        )
        assert response_job == expected_response_job

    def test_cancel(self, client):
        expected_response_job = DetailedJob.model_validate_json(mock_detailed_job_response_payload())
        client._client.request.return_value = mock_response(
            200,
            expected_response_job.model_dump_json(),
        )

        response_job = client.jobs.cancel("job_id")

        client._client.request.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/fine_tuning/jobs/job_id/cancel",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
        )
        assert response_job == expected_response_job
