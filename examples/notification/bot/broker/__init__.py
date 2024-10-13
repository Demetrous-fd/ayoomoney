from .base import shutdown, startup, _broker

from .payment import router as payment_router

_broker.include_routers(
    payment_router
)

wiring_modules = [
    "bot.broker.payment"
]
