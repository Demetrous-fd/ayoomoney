from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel, Field


class PaymentMessage(BaseModel):
    label: str = Field(...)


class PaymentCallback(CallbackData, prefix="order"):
    label: str = Field(...)

