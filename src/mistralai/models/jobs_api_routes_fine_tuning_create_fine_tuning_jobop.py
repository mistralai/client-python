"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .jobout import JobOut, JobOutTypedDict
from .legacyjobmetadataout import LegacyJobMetadataOut, LegacyJobMetadataOutTypedDict
from typing import Union


JobsAPIRoutesFineTuningCreateFineTuningJobResponseTypedDict = Union[
    LegacyJobMetadataOutTypedDict, JobOutTypedDict
]
r"""OK"""


JobsAPIRoutesFineTuningCreateFineTuningJobResponse = Union[LegacyJobMetadataOut, JobOut]
r"""OK"""
