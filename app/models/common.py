from typing import Any

import arrow
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_core.core_schema import SerializationInfo
from sqlalchemy.sql import func
from sqlalchemy_utils import ArrowType
from sqlmodel import Field

# This class is copied from the following link
# Src: https://github.com/pydantic/pydantic/issues/8737#issuecomment-1930472344
# This class is used to serialize Arrow objects in Pydantic models


class ArrowPydanticV2(arrow.Arrow):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        def validate_by_arrow(value: Any) -> arrow.Arrow:
            try:
                arr: arrow.Arrow = arrow.get(value)
                return arr
            except Exception:  # noqa: BLE001
                raise ValueError("Arrow can not parse")

        def arrow_serialization(value: arrow.Arrow, _: Any, info: SerializationInfo) -> str | arrow.Arrow:
            if info.mode == "json":
                return value.isoformat()
            return value

        return core_schema.no_info_after_validator_function(
            function=validate_by_arrow,
            schema=core_schema.any_schema(),
            serialization=core_schema.wrap_serializer_function_ser_schema(arrow_serialization, info_arg=True),
        )


class CreateAt:
    create_at: ArrowPydanticV2 = Field(
        default_factory=arrow.utcnow,
        nullable=False,
        sa_type=ArrowType,
        sa_column_kwargs={"server_default": func.now()},
    )


class UpdateAt:
    update_at: ArrowPydanticV2 = Field(
        default_factory=arrow.utcnow,
        nullable=False,
        sa_type=ArrowType,
        sa_column_kwargs={"server_default": func.now(), "onupdate": arrow.utcnow},
    )


class DatetimeMixin(UpdateAt, CreateAt):
    pass
