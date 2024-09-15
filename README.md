# ayoomoney — простая синхронная/асинхронная библиотека для работы с API ЮMoney

### Установка
```shell
pip install ayoomoney
```

### Авторизация приложения

1. Зарегистрируйте новое приложение YooMoney по ссылке https://yoomoney.ru/myservices/new 
   - В полях "Адрес сайта" и "Redirect URI" укажите адрес: http://my.localhost
   - Чекбокс "Проверять подлинность приложения (OAuth2 client_secret)" должен быть отключен
2. Получите и скопируйте `client_id` после создания приложения
3. [Получение access-токена](https://yoomoney.ru/docs/wallet/using-api/authorization/obtain-access-token)
   
   Во всех методах используются все доступные разрешения/scope, вы можете указать нужные вам разрешения
   через запятую, используя параметр `--scope`, пример: `--scope account-info,operation-details,operation-history` 

   - Автоматическое получение
   ```shell
   python -m ayoomoney.auth auto <client_id> http://my.localhost
   ```
   
   - Ручное получение
   ```shell
   python -m ayoomoney.auth simple <client_id> http://my.localhost
   ```
   Во время перенаправления по `redirect_uri` в адресной строке появится параметр `code=`.
   Скопируйте значение и вставьте его в консоль

   Если авторизация прошла успешно, в консоли отобразится Ваш access-token.
4. Сохраните access-token в [переменные окружения](https://habr.com/ru/articles/472674/), не храните токен в коде.

### Получение основной информации об аккаунте

```python
from os import environ

from ayoomoney.wallet import YooMoneyWalletAsync, YooMoneyWallet
from ayoomoney.types import AccountInfo


def sync_example():
    wallet = YooMoneyWallet(access_token=environ.get("ACCESS_TOKEN"))
    account_info: AccountInfo = wallet.account_info()
    print(account_info)
    
    wallet.close()  # Не забудьте закрыть сессию или используйте менеджер контекста


async def async_example():
    wallet = YooMoneyWalletAsync(access_token=environ.get("ACCESS_TOKEN"))
    account_info: AccountInfo = await wallet.account_info()
    print(account_info)
    
    await wallet.close()  # Не забудьте закрыть сессию или используйте менеджер контекста
   

if __name__ == "__main__":
    sync_example()

    # import asyncio
    # asyncio.run(async_example())
```

### Использование менеджера контекста
```python
from os import environ

from ayoomoney.wallet import YooMoneyWalletAsync, YooMoneyWallet
from ayoomoney.types import AccountInfo


def sync_example():
    with YooMoneyWallet(access_token=environ.get("ACCESS_TOKEN")) as wallet:
        account_info: AccountInfo = wallet.account_info()
        print(account_info)


async def async_example():
    async with YooMoneyWalletAsync(access_token=environ.get("ACCESS_TOKEN")) as wallet:
        account_info: AccountInfo = await wallet.account_info()
        print(account_info)


if __name__ == "__main__":
    sync_example()

   # import asyncio
   # asyncio.run(async_example())
```

### Создание платёжной формы и проверка оплаты

```python
from os import environ

from ayoomoney.wallet import YooMoneyWalletAsync, PaymentSource


async def main():
    async with YooMoneyWalletAsync(access_token=environ.get("ACCESS_TOKEN")) as wallet:
        payment_form = await wallet.create_payment_form(
            amount_rub=2,
            unique_label="myproject",
            payment_source=PaymentSource.YOOMONEY_WALLET,
            success_redirect_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xl"
        )
        # проверка платежа по label
        payment_is_completed: bool = await wallet.check_payment_on_successful(
            payment_form.payment_label
        )

        print(
            f"Ссылка на оплату:\n{payment_form.link_for_customer}\n\n"
            f"Форма оплачена: {'Да' if payment_is_completed else 'Нет'}"
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```

### История платежей

```python
from datetime import datetime
from os import environ

from ayoomoney.types import OperationHistoryParams, OperationHistoryParamType
from ayoomoney.wallet import YooMoneyWalletAsync


async def main():
    async with YooMoneyWalletAsync(access_token=environ.get("ACCESS_TOKEN")) as wallet:
        payments_from = datetime.strptime("15.09.2024", "%d.%m.%Y")
        params = OperationHistoryParams(
            # label="lazydeus-1",  # Получение определенного платежа по метке

            from_datetime=payments_from,  # Получение операций после 15.09.2024 00:00
            # till_datetime=payments_from  # Получение операций до 15.09.2024 00:00

            operation_type=["deposition", OperationHistoryParamType.PAYMENT],
            # Типы операций, можно использовать OperationHistoryParamType или вводить значения вручную

            records=3,  # limit, Количество операций за один запрос, по умолчанию 30
            start_record=3,  # offset, https://yoomoney.ru/docs/wallet/user-account/operation-history#filtering-logic
            
            details=True  # Показывать подробные детали операции. types.Operation -> types.OperationDetails
        )
        history = await wallet.get_operation_history(params)
        for operation in history.operations:
            print(type(operation), operation)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())


```

### Поддержка проекта
Если вы обнаружили ошибку или хотите предложить идею для улучшения проекта, создайте issue.

Если у вас есть возможность и желание внести улучшения в проект, отправляйте pull request.
