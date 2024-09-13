from httpx import Client

AUTH_URL = "https://yoomoney.ru/oauth/authorize"
TOKEN_URL = "https://yoomoney.ru/oauth/token"
DEFAULT_SCOPE = (
    "account-info",
    "operation-history",
    "operation-details",
    "incoming-transfers",
    "payment-p2p",
    "payment-shop",
)


def authorize(client_id: str, redirect_uri: str, app_permissions: list[str] = DEFAULT_SCOPE, *_):
    client = Client()
    try:
        auth_params = dict(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=" ".join(app_permissions),
            response_type="code"
        )

        response = client.post(AUTH_URL, params=auth_params)

        print(f"Перейдите по URL и подтвердите доступ для приложения\n{response.url}")
        code = input("Введите код в консоль >  ").strip()

        token_params = dict(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            grant_type="authorization_code"
        )
        response = client.post(TOKEN_URL, params=token_params)

        data = response.json()
    finally:
        client.close()

    access_token = data.get("access_token")
    if not access_token:
        print(f"Не удалось получить токен. {data.get('error', '')}")
        return

    print(f"Ваш токен — {access_token}. Сохраните его в безопасном месте!")
    return
