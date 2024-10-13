from .start import router as start_router
from .payment import router as payment_router

routes = [
    start_router,
    payment_router
]

wiring_modules = [
    "bot.handlers.payment"
]
