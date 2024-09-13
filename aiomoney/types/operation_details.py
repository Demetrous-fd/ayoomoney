from datetime import datetime

from pydantic import BaseModel, Field

from .enums import OperationDirection, OperationStatus, OperationType, RecipientType


class OperationDetails(BaseModel):
    """
    Детальная информация об операции из истории
    https://yoomoney.ru/docs/wallet/user-account/operation-details
    """
    amount: float = Field(...)
    amount_due: float | None = Field(None)
    error: str | None = Field(None)
    operation_id: str = Field(...)
    direction: OperationDirection = Field(...)
    status: OperationStatus = Field(...)
    pattern_id: str | None = Field(None)
    fee: float | None = Field(None)
    title: str = Field(...)
    sender: int | None = Field(None)
    recipient: str | None = Field(None)
    recipient_type: RecipientType | None = Field(None)
    message: str | None = Field(None)
    comment: str | None = Field(None)
    codepro: bool | None = Field(None)
    label: str | None = Field(None)
    details: str | None = Field(None)
    digital_goods: dict | None = Field(None)
    operation_type: OperationType = Field(..., alias="type")
    execution_datetime: datetime = Field(..., alias="datetime")
