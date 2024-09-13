from os import environ

from dotenv import load_dotenv

from ayoomoney.wallet import YooMoneyWallet, YooMoneyWalletAsync, PaymentSource

load_dotenv()


def sync_example():
    wallet = YooMoneyWallet(access_token=environ.get("ACCESS_TOKEN"))

    payment_form = wallet.create_payment_form(
        amount_rub=42,
        unique_label="myproject",
        payment_source=PaymentSource.YOOMONEY_WALLET,
        success_redirect_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xl"
    )
    payment_is_completed = wallet.check_payment_on_successful(payment_form.payment_label)
    print(
        f"Ссылка на оплату:\n{payment_form.link_for_customer}\n\n"
        f"Форма оплачена: {'Да' if payment_is_completed else 'Нет'}"
    )

    wallet.close()


async def async_example():
    wallet = YooMoneyWalletAsync(access_token=environ.get("ACCESS_TOKEN"))

    payment_form = await wallet.create_payment_form(
        amount_rub=42,
        unique_label="myproject",
        payment_source=PaymentSource.YOOMONEY_WALLET,
        success_redirect_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xl"
    )
    payment_is_completed = await wallet.check_payment_on_successful(payment_form.payment_label)
    print(
        f"Ссылка на оплату:\n{payment_form.link_for_customer}\n\n"
        f"Форма оплачена: {'Да' if payment_is_completed else 'Нет'}"
    )

    await wallet.close()


if __name__ == "__main__":
    # sync_example()
    import asyncio
    asyncio.run(async_example())
