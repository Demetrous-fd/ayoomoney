from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException
from ayoomoney.types import NotificationBase
from faststream.redis import RedisBroker

from notify.settings import settings

broker = RedisBroker(settings.redis_dsn)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    yield
    await broker.close()


app = FastAPI(lifespan=lifespan)


@app.post("/notification/payment")
async def payment_handler(data: Annotated[NotificationBase, Form()]):
    # https://fastapi.tiangolo.com/tutorial/request-form-models/#pydantic-models-for-forms

    is_valid_hash = data.check_sha1_hash(settings.yoomoney_notification_secret)
    if is_valid_hash is False:
        raise HTTPException(status_code=403)

    async with RedisBroker(settings.redis_dsn) as br:  # Используется для автоматического закрытия сессии
        await br.publish(data, "payment/notify")

