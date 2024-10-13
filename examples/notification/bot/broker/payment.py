from dependency_injector.wiring import Provide, inject
from faststream.redis import RedisRouter, RedisBroker
from ayoomoney.types import NotificationBase
from loguru import logger
from aiogram import Bot

from bot.repositories.payment import PaymentsRepository, GetPaymentByLabelExpression, PaymentStatus
from bot.schemes import PaymentMessage
from bot.containers import Container

router = RedisRouter()


@router.subscriber("payment/notify")
@inject
async def payment_notify_handler(
        broker: RedisBroker = Provide[Container.message_broker],
        **body: dict
):
    logger.info(f"Received message from broker: {body}")
    payment_info = NotificationBase.model_validate(body)

    if bool(payment_info.label.strip()) is False:
        return

    message = PaymentMessage(
        label=payment_info.label
    )
    async with broker:  # Используется для автоматического закрытия сессии
        await broker.publish(message, "payment")


@router.subscriber("payment")
@inject
async def payment_handler(
        bot: Bot = Provide[Container.bot],
        repository: PaymentsRepository = Provide[Container.payment_repository],
        **body: dict
):
    logger.info(f"Received message from broker: {body}")
    payment = PaymentMessage.model_validate(body)

    async with repository:  # Используется для автоматического закрытия соединения с БД
        payment = await repository.get(
            GetPaymentByLabelExpression(label=payment.label)
        )

        if payment is None:
            return

        if payment and payment.status == PaymentStatus.COMPLETED:
            await bot.send_message(
                payment.user_id,
                "Заказ был оплачен"
            )
            return

        await repository.complete(payment)

    await bot.send_message(
        payment.user_id,
        "Заказ оплачен"
    )
