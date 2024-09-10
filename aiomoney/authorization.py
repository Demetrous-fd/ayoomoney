from httpx import AsyncClient

AUTH_URL = "https://yoomoney.ru/oauth/authorize"
TOKEN_URL = "https://yoomoney.ru/oauth/token"


async def authorize_app(client_id, redirect_uri, app_permissions: list[str, ...]):
    client = AsyncClient()

    auth_params = dict(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=app_permissions,
        response_type="code"
    )
    response = await client.post(AUTH_URL, params=auth_params)

    print(f"Перейдите по URL и подтвердите доступ для приложения\n{response.url}")
    code = input("Введите код в консоль >  ").strip()

    token_params = dict(
        code=code,
        client_id=client_id,
        redirect_uri=redirect_uri,
        grant_type="authorization_code"
    )
    response = await client.post(TOKEN_URL, params=token_params)
    await client.aclose()

    data = response.json()

    access_token = data.get("access_token")
    if not access_token:
        print(f"Не удалось получить токен. {data.get('error', '')}")
        return

    print(f"Ваш токен — {access_token}. Сохраните его в безопасном месте!")
    return
