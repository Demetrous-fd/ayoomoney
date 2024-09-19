from pydantic import BaseModel, Field


class PaymentForm(BaseModel):
    link_for_customer: str = Field(...)
    payment_label: str = Field(...)
