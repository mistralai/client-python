from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class TrainingParameters(BaseModel):
    training_steps: int = Field(1800, le=10000, ge=1)
    learning_rate: float = Field(1.0e-4, le=1, ge=1.0e-8)


class WandbIntegration(BaseModel):
    type: Literal["wandb"] = "wandb"
    project: str
    name: Union[str, None] = None
    run_name: Union[str, None] = None


class WandbIntegrationIn(WandbIntegration):
    api_key: str


Integration = Annotated[Union[WandbIntegration], Field(discriminator="type")]
IntegrationIn = Annotated[Union[WandbIntegrationIn], Field(discriminator="type")]


class JobMetadata(BaseModel):
    object: Literal["job.metadata"] = "job.metadata"
    training_steps: int
    train_tokens_per_step: int
    data_tokens: int
    train_tokens: int
    epochs: float
    expected_duration_seconds: Optional[int]
    cost: Optional[float] = None
    cost_currency: Optional[str] = None


class Job(BaseModel):
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


class Event(BaseModel):
    name: str
    data: Union[dict, None] = None
    created_at: int


class Metric(BaseModel):
    train_loss: Union[float, None] = None
    valid_loss: Union[float, None] = None
    valid_mean_token_accuracy: Union[float, None] = None


class Checkpoint(BaseModel):
    metrics: Metric
    step_number: int
    created_at: int


class JobQueryFilter(BaseModel):
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


class Jobs(BaseModel):
    data: list[Job] = []
    object: Literal["list"]
