from pydantic import BaseModel, Field


class BalanceDetails(BaseModel):
    total: int = Field(...)
    available: int = Field(...)
    deposition_pending: int | None = Field(None)
    blocked: int | None = Field(None)
    debt: int | None = Field(None)
    hold: int | None = Field(None)


class LinkedCard(BaseModel):
    pan_fragment: str = Field(...)
    card_type: str = Field(None, alias="type")


class AccountInfo(BaseModel):
    """
    Получение информации о состоянии счета пользователя
    https://yoomoney.ru/docs/wallet/user-account/account-info
    """
    account: str = Field(...)  # номер счета
    balance: int = Field(...)  # баланс счета
    currency: str = Field(...)  # код валюты счета
    account_type: str = Field(...)
    account_status: str = Field(...)
    balance_details: BalanceDetails | None = Field(None)
    cards_linked: list[LinkedCard] | None = Field(None)
