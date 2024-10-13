from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton


def create_start_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Создать тестовой платеж")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    return keyboard
