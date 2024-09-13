from datetime import datetime

from pydantic import BaseModel, Field

from .enums import OperationDirection, OperationStatus, OperationType
from .operation_details import OperationDetails


class Operation(BaseModel):
    """
    Описание платежной операции
    https://yoomoney.ru/docs/wallet/user-account/operation-history#response-operation
    """
    operation_id: str = Field(...)
    status: OperationStatus = Field(...)
    execution_datetime: datetime = Field(..., alias="datetime")
    title: str = Field(...)
    pattern_id: str | None = Field(None)
    direction: OperationDirection = Field(...)
    amount: float = Field(...)
    label: str | None = Field(None)
    operation_type: OperationType = Field(..., alias="type")


class OperationHistory(BaseModel):
    error: str | None = Field(None)
    next_record: int | None = Field(None)
    operations: list[Operation | OperationDetails] = Field(...)
