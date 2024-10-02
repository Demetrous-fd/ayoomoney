from enum import StrEnum


class PaymentSource(StrEnum):
    BANK_CARD = "AC"
    YOOMONEY_WALLET = "PC"


class OperationDirection(StrEnum):
    IN = "in"
    OUT = "out"


class OperationStatus(StrEnum):
    SUCCESS = "success"
    REFUSED = "refused"
    IN_PROGRESS = "in_progress"


class OperationType(StrEnum):
    PAYMENT_SHOP = "payment-shop"
    OUTGOING_TRANSFER = "outgoing-transfer"
    DEPOSITION = "deposition"
    INCOMING_TRANSFER = "incoming-transfer"


class OperationHistoryParamType(StrEnum):
    DEPOSITION = "deposition"
    PAYMENT = "payment"


class RecipientType(StrEnum):
    ACCOUNT = "account"
    PHONE = "phone"
    EMAIL = "email"


class NotificationType(StrEnum):
    P2P_INCOMING = "p2p-incoming"
    CARD_INCOMING = "card-incoming"
