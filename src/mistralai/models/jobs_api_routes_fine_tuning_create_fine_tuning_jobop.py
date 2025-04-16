"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .classifierjobout import ClassifierJobOut, ClassifierJobOutTypedDict
from .completionjobout import CompletionJobOut, CompletionJobOutTypedDict
from .legacyjobmetadataout import LegacyJobMetadataOut, LegacyJobMetadataOutTypedDict
from mistralai.utils import get_discriminator
from pydantic import Discriminator, Tag
from typing import Union
from typing_extensions import Annotated, TypeAliasType


Response1TypedDict = TypeAliasType(
    "Response1TypedDict", Union[ClassifierJobOutTypedDict, CompletionJobOutTypedDict]
)


Response1 = Annotated[
    Union[
        Annotated[ClassifierJobOut, Tag("classifier")],
        Annotated[CompletionJobOut, Tag("completion")],
    ],
    Discriminator(lambda m: get_discriminator(m, "job_type", "job_type")),
]


JobsAPIRoutesFineTuningCreateFineTuningJobResponseTypedDict = TypeAliasType(
    "JobsAPIRoutesFineTuningCreateFineTuningJobResponseTypedDict",
    Union[LegacyJobMetadataOutTypedDict, Response1TypedDict],
)
r"""OK"""


JobsAPIRoutesFineTuningCreateFineTuningJobResponse = TypeAliasType(
    "JobsAPIRoutesFineTuningCreateFineTuningJobResponse",
    Union[LegacyJobMetadataOut, Response1],
)
r"""OK"""
