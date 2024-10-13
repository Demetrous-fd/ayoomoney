from faststream.redis import RedisBroker

from bot.settings import settings


_broker = RedisBroker(settings.redis_dsn, logger=None)


async def startup():
    await _broker.start()


async def shutdown():
    await _broker.close()
