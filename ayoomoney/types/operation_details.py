from pydantic import Field

from .enums import RecipientType
from .operation import Operation


class OperationDetails(Operation):
    """
    Детальная информация об операции из истории
    https://yoomoney.ru/docs/wallet/user-account/operation-details
    """
    amount_due: float | None = Field(None)
    error: str | None = Field(None)
    fee: float | None = Field(None)
    sender: int | None = Field(None)
    recipient: str | None = Field(None)
    recipient_type: RecipientType | None = Field(None)
    message: str | None = Field(None)
    comment: str | None = Field(None)
    codepro: bool | None = Field(None)
    details: str | None = Field(None)
    digital_goods: dict | None = Field(None)
