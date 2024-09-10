from datetime import datetime

from pydantic import BaseModel, Field

from .enums import OperationDirection


class OperationDetails(BaseModel):
    """
    Детальная информация об операции из истории
    https://yoomoney.ru/docs/wallet/user-account/operation-details
    """
    amount: int = Field(...)
    amount_due: int | None = Field(None)
    error: str | None = Field(None)
    operation_id: str = Field(...)
    direction: OperationDirection = Field(...)
    status: str = Field(...)
    pattern_id: str | None = Field(None)
    fee: int | None = Field(None)
    title: str = Field(...)
    sender: int | None = Field(None)
    recipient: str | None = Field(None)
    recipient_type: str | None = Field(None)
    message: str | None = Field(None)
    comment: str | None = Field(None)
    label: str | None = Field(None)
    details: str | None = Field(None)
    operation_type: str = Field(..., alias="type")
    operation_datetime: datetime = Field(..., alias="datetime")
