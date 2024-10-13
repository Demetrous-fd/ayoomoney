from enum import StrEnum
from decimal import Decimal

from sqlalchemy import Column, BigInteger, DateTime, DECIMAL, String, Enum, Integer
from sqlalchemy.sql import func

from bot.models.base import Base


class PaymentStatus(StrEnum):
    COMPLETED = "completed"
    UNCOMPLETED = "uncompleted"


class PaymentHistory(Base):
    __tablename__ = "payments_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, index=True)
    amount = Column(DECIMAL())
    label = Column(String(64), index=True)
    status = Column(Enum(PaymentStatus))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
