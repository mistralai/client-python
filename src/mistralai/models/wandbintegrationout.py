"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from mistralai.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
import pydantic
from pydantic import model_serializer
from typing import Final, Literal, Optional, TypedDict
from typing_extensions import Annotated, NotRequired


Type = Literal["wandb"]


class WandbIntegrationOutTypedDict(TypedDict):
    project: str
    r"""The name of the project that the new run will be created under."""
    name: NotRequired[Nullable[str]]
    r"""A display name to set for the run. If not set, will use the job ID as the name."""
    run_name: NotRequired[Nullable[str]]


class WandbIntegrationOut(BaseModel):
    project: str
    r"""The name of the project that the new run will be created under."""

    # fmt: off
    TYPE: Annotated[Final[Optional[Type]], pydantic.Field(alias="type")] = "wandb" # type: ignore
    # fmt: on

    name: OptionalNullable[str] = UNSET
    r"""A display name to set for the run. If not set, will use the job ID as the name."""

    run_name: OptionalNullable[str] = UNSET

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = ["type", "name", "run_name"]
        nullable_fields = ["name", "run_name"]
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
