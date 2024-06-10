from typing import Any, TypeVar

import pydantic
from pydantic import BaseModel

Model = TypeVar("Model", bound="BaseModel")
IS_V1 = pydantic.VERSION.startswith("1.")


class BackwardCompatibleBaseModel(BaseModel):
    def model_dump(self, *args: Any, **kwargs: Any) -> Any:
        if IS_V1:
            return self.dict(*args, **kwargs)
        return super().model_dump(*args, **kwargs)  # type: ignore

    @classmethod
    def model_validate_json(cls: type[Model], *args: Any, **kwargs: Any) -> Model:
        if IS_V1:
            return cls.parse_raw(*args, **kwargs)
        return super().model_validate_json(*args, **kwargs)  # type: ignore

    def model_dump_json(self, *args: Any, **kwargs: Any) -> str:
        if IS_V1:
            return self.json(*args, **kwargs)
        return super().model_dump_json(*args, **kwargs)  # type: ignore
