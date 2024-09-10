from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PaymentForm:
    link_for_customer: str
    payment_label: str
