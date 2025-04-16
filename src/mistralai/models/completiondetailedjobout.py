"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .checkpointout import CheckpointOut, CheckpointOutTypedDict
from .completiontrainingparameters import (
    CompletionTrainingParameters,
    CompletionTrainingParametersTypedDict,
)
from .eventout import EventOut, EventOutTypedDict
from .githubrepositoryout import GithubRepositoryOut, GithubRepositoryOutTypedDict
from .jobmetadataout import JobMetadataOut, JobMetadataOutTypedDict
from .wandbintegrationout import WandbIntegrationOut, WandbIntegrationOutTypedDict
from mistralai.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
from mistralai.utils import validate_const
import pydantic
from pydantic import model_serializer
from pydantic.functional_validators import AfterValidator
from typing import List, Literal, Optional
from typing_extensions import Annotated, NotRequired, TypedDict


CompletionDetailedJobOutStatus = Literal[
    "QUEUED",
    "STARTED",
    "VALIDATING",
    "VALIDATED",
    "RUNNING",
    "FAILED_VALIDATION",
    "FAILED",
    "SUCCESS",
    "CANCELLED",
    "CANCELLATION_REQUESTED",
]

CompletionDetailedJobOutObject = Literal["job"]

CompletionDetailedJobOutIntegrationsTypedDict = WandbIntegrationOutTypedDict


CompletionDetailedJobOutIntegrations = WandbIntegrationOut


CompletionDetailedJobOutJobType = Literal["completion"]

CompletionDetailedJobOutRepositoriesTypedDict = GithubRepositoryOutTypedDict


CompletionDetailedJobOutRepositories = GithubRepositoryOut


class CompletionDetailedJobOutTypedDict(TypedDict):
    id: str
    auto_start: bool
    model: str
    r"""The name of the model to fine-tune."""
    status: CompletionDetailedJobOutStatus
    created_at: int
    modified_at: int
    training_files: List[str]
    hyperparameters: CompletionTrainingParametersTypedDict
    validation_files: NotRequired[Nullable[List[str]]]
    object: CompletionDetailedJobOutObject
    fine_tuned_model: NotRequired[Nullable[str]]
    suffix: NotRequired[Nullable[str]]
    integrations: NotRequired[
        Nullable[List[CompletionDetailedJobOutIntegrationsTypedDict]]
    ]
    trained_tokens: NotRequired[Nullable[int]]
    metadata: NotRequired[Nullable[JobMetadataOutTypedDict]]
    job_type: CompletionDetailedJobOutJobType
    repositories: NotRequired[List[CompletionDetailedJobOutRepositoriesTypedDict]]
    events: NotRequired[List[EventOutTypedDict]]
    r"""Event items are created every time the status of a fine-tuning job changes. The timestamped list of all events is accessible here."""
    checkpoints: NotRequired[List[CheckpointOutTypedDict]]


class CompletionDetailedJobOut(BaseModel):
    id: str

    auto_start: bool

    model: str
    r"""The name of the model to fine-tune."""

    status: CompletionDetailedJobOutStatus

    created_at: int

    modified_at: int

    training_files: List[str]

    hyperparameters: CompletionTrainingParameters

    validation_files: OptionalNullable[List[str]] = UNSET

    OBJECT: Annotated[
        Annotated[
            Optional[CompletionDetailedJobOutObject],
            AfterValidator(validate_const("job")),
        ],
        pydantic.Field(alias="object"),
    ] = "job"

    fine_tuned_model: OptionalNullable[str] = UNSET

    suffix: OptionalNullable[str] = UNSET

    integrations: OptionalNullable[List[CompletionDetailedJobOutIntegrations]] = UNSET

    trained_tokens: OptionalNullable[int] = UNSET

    metadata: OptionalNullable[JobMetadataOut] = UNSET

    JOB_TYPE: Annotated[
        Annotated[
            Optional[CompletionDetailedJobOutJobType],
            AfterValidator(validate_const("completion")),
        ],
        pydantic.Field(alias="job_type"),
    ] = "completion"

    repositories: Optional[List[CompletionDetailedJobOutRepositories]] = None

    events: Optional[List[EventOut]] = None
    r"""Event items are created every time the status of a fine-tuning job changes. The timestamped list of all events is accessible here."""

    checkpoints: Optional[List[CheckpointOut]] = None

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = [
            "validation_files",
            "object",
            "fine_tuned_model",
            "suffix",
            "integrations",
            "trained_tokens",
            "metadata",
            "job_type",
            "repositories",
            "events",
            "checkpoints",
        ]
        nullable_fields = [
            "validation_files",
            "fine_tuned_model",
            "suffix",
            "integrations",
            "trained_tokens",
            "metadata",
        ]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)
            serialized.pop(k, None)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m
