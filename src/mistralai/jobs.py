from datetime import datetime
from typing import Any, Optional, Union

from mistralai.exceptions import (
    MistralException,
)
from mistralai.models.jobs import DetailedJob, IntegrationIn, Job, JobMetadata, JobQueryFilter, Jobs, TrainingParameters


class JobsClient:
    def __init__(self, client: Any):
        self.client = client

    def create(
        self,
        model: str,
        training_files: Union[list[str], None] = None,
        validation_files: Union[list[str], None] = None,
        hyperparameters: TrainingParameters = TrainingParameters(
            training_steps=1800,
            learning_rate=1.0e-4,
        ),
        suffix: Union[str, None] = None,
        integrations: Union[set[IntegrationIn], None] = None,
        training_file: Union[str, None] = None,  # Deprecated: Added for compatibility with OpenAI API
        validation_file: Union[str, None] = None,  # Deprecated: Added for compatibility with OpenAI API
        dry_run: bool = False,
    ) -> Union[Job, JobMetadata]:
        # Handle deprecated arguments
        if not training_files and training_file:
            training_files = [training_file]
        if not validation_files and validation_file:
            validation_files = [validation_file]
        single_response = self.client._request(
            method="post",
            json={
                "model": model,
                "training_files": training_files,
                "validation_files": validation_files,
                "hyperparameters": hyperparameters.dict(),
                "suffix": suffix,
                "integrations": integrations,
            },
            path="v1/fine_tuning/jobs",
            params={"dry_run": dry_run},
        )
        for response in single_response:
            return Job(**response) if not dry_run else JobMetadata(**response)
        raise MistralException("No response received")

    def retrieve(self, job_id: str) -> DetailedJob:
        single_response = self.client._request(method="get", path=f"v1/fine_tuning/jobs/{job_id}", json={})
        for response in single_response:
            return DetailedJob(**response)
        raise MistralException("No response received")

    def list(
        self,
        page: int = 0,
        page_size: int = 10,
        model: Optional[str] = None,
        created_after: Optional[datetime] = None,
        created_by_me: Optional[bool] = None,
        status: Optional[str] = None,
        wandb_project: Optional[str] = None,
        wandb_name: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> Jobs:
        query_params = JobQueryFilter(
            page=page,
            page_size=page_size,
            model=model,
            created_after=created_after,
            created_by_me=created_by_me,
            status=status,
            wandb_project=wandb_project,
            wandb_name=wandb_name,
            suffix=suffix,
        ).model_dump(exclude_none=True)
        single_response = self.client._request(method="get", params=query_params, path="v1/fine_tuning/jobs", json={})
        for response in single_response:
            return Jobs(**response)
        raise MistralException("No response received")

    def cancel(self, job_id: str) -> DetailedJob:
        single_response = self.client._request(method="post", path=f"v1/fine_tuning/jobs/{job_id}/cancel", json={})
        for response in single_response:
            return DetailedJob(**response)
        raise MistralException("No response received")


class JobsAsyncClient:
    def __init__(self, client: Any):
        self.client = client

    async def create(
        self,
        model: str,
        training_files: Union[list[str], None] = None,
        validation_files: Union[list[str], None] = None,
        hyperparameters: TrainingParameters = TrainingParameters(
            training_steps=1800,
            learning_rate=1.0e-4,
        ),
        suffix: Union[str, None] = None,
        integrations: Union[set[IntegrationIn], None] = None,
        training_file: Union[str, None] = None,  # Deprecated: Added for compatibility with OpenAI API
        validation_file: Union[str, None] = None,  # Deprecated: Added for compatibility with OpenAI API
        dry_run: bool = False,
    ) -> Union[Job, JobMetadata]:
        # Handle deprecated arguments
        if not training_files and training_file:
            training_files = [training_file]
        if not validation_files and validation_file:
            validation_files = [validation_file]

        single_response = self.client._request(
            method="post",
            json={
                "model": model,
                "training_files": training_files,
                "validation_files": validation_files,
                "hyperparameters": hyperparameters.dict(),
                "suffix": suffix,
                "integrations": integrations,
            },
            path="v1/fine_tuning/jobs",
            params={"dry_run": dry_run},
        )
        async for response in single_response:
            return Job(**response) if not dry_run else JobMetadata(**response)
        raise MistralException("No response received")

    async def retrieve(self, job_id: str) -> DetailedJob:
        single_response = self.client._request(method="get", path=f"v1/fine_tuning/jobs/{job_id}", json={})
        async for response in single_response:
            return DetailedJob(**response)
        raise MistralException("No response received")

    async def list(
        self,
        page: int = 0,
        page_size: int = 10,
        model: Optional[str] = None,
        created_after: Optional[datetime] = None,
        created_by_me: Optional[bool] = None,
        status: Optional[str] = None,
        wandb_project: Optional[str] = None,
        wandb_name: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> Jobs:
        query_params = JobQueryFilter(
            page=page,
            page_size=page_size,
            model=model,
            created_after=created_after,
            created_by_me=created_by_me,
            status=status,
            wandb_project=wandb_project,
            wandb_name=wandb_name,
            suffix=suffix,
        ).model_dump(exclude_none=True)
        single_response = self.client._request(method="get", path="v1/fine_tuning/jobs", params=query_params, json={})
        async for response in single_response:
            return Jobs(**response)
        raise MistralException("No response received")

    async def cancel(self, job_id: str) -> DetailedJob:
        single_response = self.client._request(method="post", path=f"v1/fine_tuning/jobs/{job_id}/cancel", json={})
        async for response in single_response:
            return DetailedJob(**response)
        raise MistralException("No response received")
