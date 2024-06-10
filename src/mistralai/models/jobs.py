from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import Field

from mistralai.models.base_model import BackwardCompatibleBaseModel


class TrainingParameters(BackwardCompatibleBaseModel):
    training_steps: int = Field(1800, le=10000, ge=1)
    learning_rate: float = Field(1.0e-4, le=1, ge=1.0e-8)


class WandbIntegration(BackwardCompatibleBaseModel):
    type: Literal["wandb"] = "wandb"
    project: str
    name: Union[str, None] = None
    run_name: Union[str, None] = None


class WandbIntegrationIn(WandbIntegration):
    api_key: str


Integration = Union[WandbIntegration]
IntegrationIn = Union[WandbIntegrationIn]


class JobMetadata(BackwardCompatibleBaseModel):
    object: Literal["job.metadata"] = "job.metadata"
    training_steps: int
    train_tokens_per_step: int
    data_tokens: int
    train_tokens: int
    epochs: float
    expected_duration_seconds: Optional[int]


class Job(BackwardCompatibleBaseModel):
    id: str
    hyperparameters: TrainingParameters
    fine_tuned_model: Union[str, None]
    model: str
    status: Literal[
        "QUEUED",
        "STARTED",
        "RUNNING",
        "FAILED",
        "SUCCESS",
        "CANCELLED",
        "CANCELLATION_REQUESTED",
    ]
    job_type: str
    created_at: int
    modified_at: int
    training_files: list[str]
    validation_files: Union[list[str], None] = []
    object: Literal["job"]
    integrations: List[Integration] = []


class Event(BackwardCompatibleBaseModel):
    name: str
    data: Union[dict, None] = None
    created_at: int


class Metric(BackwardCompatibleBaseModel):
    train_loss: Union[float, None] = None
    valid_loss: Union[float, None] = None
    valid_mean_token_accuracy: Union[float, None] = None


class Checkpoint(BackwardCompatibleBaseModel):
    metrics: Metric
    step_number: int
    created_at: int


class JobQueryFilter(BackwardCompatibleBaseModel):
    page: int = 0
    page_size: int = 100
    model: Optional[str] = None
    created_after: Optional[datetime] = None
    created_by_me: Optional[bool] = None
    status: Optional[str] = None
    wandb_project: Optional[str] = None
    wandb_name: Optional[str] = None
    suffix: Optional[str] = None


class DetailedJob(Job):
    events: list[Event] = []
    checkpoints: list[Checkpoint] = []
    estimated_start_time: Optional[int] = None


class Jobs(BackwardCompatibleBaseModel):
    data: list[Job] = []
    object: Literal["list"]
