from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_order_keyboard(form_url: str, callback_data: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(
        text="Оплатить", url=form_url
    ))
    kb.adjust(1)
    kb.button(
        text="Проверить оплату", callback_data=callback_data
    )
    kb.adjust(1)
    return kb.as_markup()
