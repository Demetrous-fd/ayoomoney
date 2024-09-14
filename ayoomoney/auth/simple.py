from .base import Authorization, DEFAULT_SCOPE
from ayoomoney.errors import CreateTokenError


def authorize(client_id: str, redirect_uri: str, scope: list[str] = DEFAULT_SCOPE, *_):
    access_token = ""
    auth = Authorization(client_id, redirect_uri)
    try:
        url = auth.authorization_request(scope=scope)

        print(f"Перейдите по URL и подтвердите доступ для приложения\n{url}")
        code = input("Введите код из адресной строки в консоль >>>  ").strip()

        access_token = auth.get_access_token(code)
    except CreateTokenError as e:
        print(e)
    finally:
        auth.close()

    if not access_token:
        return

    print(f"Ваш токен — {access_token}. Сохраните его в безопасном месте!")
    return
