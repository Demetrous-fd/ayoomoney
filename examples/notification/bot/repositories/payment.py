from sqlalchemy import select

from bot.models.payment import PaymentStatus, PaymentHistory
from .base import BaseQueryExpression, BaseDBRepository


class GetPaymentByLabelExpression(BaseQueryExpression):
    def __init__(self, label: str):
        self.label = label

    def complete(self):
        return PaymentHistory.label == self.label


class PaymentsRepository(BaseDBRepository):
    async def get(self, expression: BaseQueryExpression) -> PaymentHistory | None:
        statement = select(PaymentHistory).where(
            expression.complete()
        )
        query = await self.session.execute(statement)
        result = query.scalar()
        return result

    async def create(
            self,
            user_id: int,
            label: str,
            amount: float
    ) -> PaymentHistory:
        history = PaymentHistory(
            user_id=user_id,
            label=label,
            amount=amount,
            status=PaymentStatus.UNCOMPLETED
        )
        self.session.add(history)
        await self.session.commit()
        return history

    async def complete(
            self,
            payment: PaymentHistory
    ):
        payment.status = PaymentStatus.COMPLETED
        await self.session.commit()
