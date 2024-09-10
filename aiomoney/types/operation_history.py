from datetime import datetime

from pydantic import BaseModel, Field

from .enums import OperationDirection


class Operation(BaseModel):
    """
    Описание платежной операции
    https://yoomoney.ru/docs/wallet/user-account/operation-history#response-operation
    """
    operation_id: str = Field(...)
    status: str = Field(...)
    execution_datetime: datetime = Field(..., alias="datetime")
    title: str = Field(...)
    pattern_id: str | None = Field(None)
    direction: OperationDirection = Field(...)
    amount: int = Field(...)
    label: str | None = Field(None)
    operation_type: str = Field(..., alias="type")
