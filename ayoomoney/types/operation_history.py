from datetime import datetime

from pydantic import BaseModel, Field, conint, field_serializer

from .operation import Operation
from .enums import OperationHistoryParamType
from .operation_details import OperationDetails
from .utils import convert_datetime_to_iso_8601


class OperationHistory(BaseModel):
    error: str | None = Field(None)
    next_record: int | None = Field(None)
    operations: list[Operation | OperationDetails] = Field(...)


class OperationHistoryParams(BaseModel):
    operation_type: list[OperationHistoryParamType] | None = Field(default=None, serialization_alias="type")
    label: str | None = Field(default=None)
    from_datetime: datetime | None = Field(default=None, serialization_alias="from")
    till_datetime: datetime | None = Field(default=None, serialization_alias="till")
    start_record: int | None = Field(default=None)
    records: conint(ge=1, le=100) | None = Field(default=None)
    details: bool | None = Field(default=None)

    @field_serializer("from_datetime", "till_datetime")
    def convert_datetime_to_iso8601(self, v: datetime, _info) -> str:
        return convert_datetime_to_iso_8601(v)

    @field_serializer("operation_type")
    def convert_types(self, v: list[str], _info) -> str:
        return " ".join(v)

    @field_serializer("start_record")
    def convert_to_string(self, v: int, _info) -> str:
        return str(v)
