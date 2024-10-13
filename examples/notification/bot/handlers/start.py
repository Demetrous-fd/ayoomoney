from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

from bot.keyboards import create_start_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(
        message: Message,
        **kwargs
):
    keyboard = create_start_keyboard()
    await message.answer("Привет 🖐", reply_markup=keyboard)
