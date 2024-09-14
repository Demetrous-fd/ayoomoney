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

### Получение основной информации об аккаунте

```python
from ayoomoney.types import AccountInfo, OperationHistory, OperationDetails
from ayoomoney.wallet import YooMoneyWalletAsync, YooMoneyWallet


def sync_example():
   wallet = YooMoneyWallet(access_token="ACCESS_TOKEN")

   account_info: AccountInfo = wallet.account_info()
   operation_history: OperationHistory = wallet.get_operation_history()
   operation_details: OperationDetails = wallet.get_operation_details(operation_id="42")
    
   wallet.close()

async def async_example():
   wallet = YooMoneyWalletAsync(access_token="ACCESS_TOKEN")

   account_info: AccountInfo = await wallet.account_info()
   operation_history: OperationHistory = await wallet.get_operation_history()
   operation_details: OperationDetails = await wallet.get_operation_details(operation_id="42")
   
   await wallet.close()
   

if __name__ == "__main__":
   sync_example()

   # import asyncio
   # asyncio.run(async_example())
```

### Создание платёжной формы и проверка оплаты

```python
import asyncio
from ayoomoney.wallet import YooMoneyWalletAsync, PaymentSource


async def main():
   wallet = YooMoneyWalletAsync(access_token="ACCESS_TOKEN")

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
   
   await wallet.close()


if __name__ == "__main__":
   asyncio.run(main())

```

### Поддержка проекта
Если вы обнаружили ошибку или хотите предложить идею для улучшения проекта, создайте issue.

Если у вас есть возможность и желание внести улучшения в проект, отправляйте pull request.
