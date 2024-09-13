from datetime import datetime

from pydantic import BaseModel, Field

from .enums import OperationDirection, OperationStatus, OperationType


class Operation(BaseModel):
    """
    Описание платежной операции
    https://yoomoney.ru/docs/wallet/user-account/operation-history#response-operation
    """
    operation_id: str = Field(...)
    status: OperationStatus = Field(...)
    datetime: datetime = Field(...)
    title: str = Field(...)
    pattern_id: str | None = Field(None)
    direction: OperationDirection = Field(...)
    amount: float = Field(...)
    label: str | None = Field(None)
    type: OperationType = Field(...)


class OperationHistory(BaseModel):
    error: str = Field(...)
    next_record: int = Field(...)
    operations: list[Operation] = Field(...)
