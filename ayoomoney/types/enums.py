from enum import Enum


class PaymentSource(str, Enum):
    BANK_CARD = "AC"
    YOOMONEY_WALLET = "PC"


class OperationDirection(str, Enum):
    IN = "in"
    OUT = "out"


class OperationStatus(str, Enum):
    SUCCESS = "success"
    REFUSED = "refused"
    IN_PROGRESS = "in_progress"


class OperationType(str, Enum):
    PAYMENT_SHOP = "payment-shop"
    OUTGOING_TRANSFER = "outgoing-transfer"
    DEPOSITION = "deposition"
    INCOMING_TRANSFER = "incoming-transfer"


class OperationHistoryParamType(str, Enum):
    DEPOSITION = "deposition"
    PAYMENT = "payment"


class RecipientType(str, Enum):
    ACCOUNT = "account"
    PHONE = "phone"
    EMAIL = "email"
