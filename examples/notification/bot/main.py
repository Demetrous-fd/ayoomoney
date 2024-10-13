import asyncio
import logging

from dependency_injector.wiring import Provide, inject
from aiogram import Bot, Dispatcher

from bot.logger import InterceptHandler
from bot.containers import Container
from bot.settings import settings
from bot import broker, handlers

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)


def init_container():
    # Инициализация зависимостей
    container = Container()

    # Установка значений конфига
    container.config.telegram_token.from_value(settings.telegram_token)
    container.config.yoomoney_token.from_value(settings.yoomoney_token)
    container.config.database_dsn.from_value(settings.database_dsn)
    container.config.redis_dsn.from_value(settings.redis_dsn)

    # Указание пути до модулей, которые используют внедрение зависимостей
    container.wire(
        modules=[
            __name__,
            *broker.wiring_modules,  # Находиться в broker.__init__
            *handlers.wiring_modules,  # Находиться в handlers.__init__
        ],
    )


@inject
async def init_bot(bot: Bot = Provide[Container.bot]):
    dp = Dispatcher()

    dp.startup.register(broker.startup)
    dp.shutdown.register(broker.shutdown)

    dp.include_routers(*handlers.routes)

    await dp.start_polling(bot)


async def main():
    init_container()
    await init_bot()


if __name__ == "__main__":
    asyncio.run(main())
