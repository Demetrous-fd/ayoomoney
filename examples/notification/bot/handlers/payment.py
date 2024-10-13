from uuid import uuid4

from dependency_injector.wiring import inject, Provide
from aiogram.types import Message, CallbackQuery
from ayoomoney import YooMoneyWalletAsync
from faststream.redis import RedisBroker
from aiogram import Router, F

from bot.schemes import PaymentMessage, PaymentCallback
from bot.keyboards import create_order_keyboard
from bot.repositories import PaymentsRepository
from bot.containers import Container

router = Router()


@router.message(F.text.lower() == "создать тестовой платеж")
@inject
async def create_payment_handler(
        message: Message,
        repository: PaymentsRepository = Provide[Container.payment_repository],
        wallet: YooMoneyWalletAsync = Provide[Container.yoomoney_client]
):
    label = str(uuid4())
    amount = 2  # Минимальная сумма платежа в yoomoney

    async with repository:  # Используется для автоматического закрытия соединения с БД
        await repository.create(
            message.chat.id,
            label=label,
            amount=amount
        )

    async with wallet:  # Используется для автоматического закрытия сессии
        form = await wallet.create_payment_form(amount, label)

    callback_data = PaymentCallback(label=label)
    keyboard = create_order_keyboard(form.link_for_customer, callback_data.pack())

    await message.answer(
        "Тестовый платеж на 2 руб.",
        reply_markup=keyboard
    )


@router.callback_query(PaymentCallback.filter())
@inject
async def check_payment_callback(
        query: CallbackQuery,
        callback_data: PaymentCallback,
        wallet: YooMoneyWalletAsync = Provide[Container.yoomoney_client],
        broker: RedisBroker = Provide[Container.message_broker],
        **kwargs
):
    if bool(callback_data.label.strip()) is False:
        return

    async with wallet:  # Используется для автоматического закрытия сессии
        payment_is_completed: bool = await wallet.check_payment_on_successful(callback_data.label)

    if payment_is_completed is False:
        await query.message.answer(
            "Заказ не оплачен"
        )
        return

    message = PaymentMessage(label=callback_data.label)
    async with broker:  # Используется для автоматического закрытия сессии
        await broker.publish(message, "payment")
