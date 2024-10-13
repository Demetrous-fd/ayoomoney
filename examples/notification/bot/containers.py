from dependency_injector import containers, providers
from ayoomoney import YooMoneyWalletAsync
from faststream.redis import RedisBroker
from loguru import logger
from aiogram import Bot

from bot import repositories, database


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    bot = providers.Singleton(
        Bot,
        token=config.telegram_token
    )
    database_pool = providers.Resource(
        database.create_connection_pool,
        database_dsn=config.database_dsn
    )
    database_session = providers.Factory(
        database.create_connection,
        session_pool=database_pool
    )
    yoomoney_client = providers.Factory(
        YooMoneyWalletAsync,
        access_token=config.yoomoney_token
    )
    message_broker = providers.Factory(
        RedisBroker,
        url=config.redis_dsn
    )

    payment_repository = providers.Factory(
        repositories.PaymentsRepository,
        session=database_session
    )
