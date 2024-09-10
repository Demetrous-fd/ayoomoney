from enum import Enum


class PaymentSource(str, Enum):
    BANK_CARD = "AC"
    YOOMONEY_WALLET = "PC"


class OperationDirection(str, Enum):
    IN = "in"
    OUT = "out"
