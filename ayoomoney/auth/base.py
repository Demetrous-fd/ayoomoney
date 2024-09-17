from typing import Literal

from httpx import Client, AsyncClient, Response

from ayoomoney.errors import CreateTokenError

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


class _BaseAuthorization:
    def __init__(self, client_id: str, redirect_uri: str):
        self.client_id = client_id
        self.redirect_uri = redirect_uri

    def _process_get_access_token(self, response: Response) -> str | None:
        data = response.json()
        access_token = data.get("access_token", None)
        error = data.get("error", None)
        if error or not access_token:
            if not access_token:
                raise CreateTokenError(error="invalid_request")
            raise CreateTokenError(error=error)
        return access_token


class Authorization(_BaseAuthorization):
    def __init__(self, client_id: str, redirect_uri: str):
        super().__init__(client_id, redirect_uri)
        self.client = Client(
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

    def close(self):
        self.client.close()

    def authorization_request(
            self,
            response_type: Literal["code"] = "code",
            scope: list[str] = DEFAULT_SCOPE,
            instance_name: str | None = None
    ) -> str:
        auth_params = dict(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=" ".join(scope),
            response_type=response_type
        )
        if instance_name:
            auth_params["instance_name"] = instance_name

        response = self.client.post(AUTH_URL, params=auth_params)
        return str(response.url)

    def get_access_token(
            self,
            code: str,
            grant_type: Literal["authorization_code"] = "authorization_code",
            client_secret: str | None = None
    ) -> str | None:
        token_params = dict(
            code=code,
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            grant_type=grant_type
        )
        if client_secret:
            token_params["client_secret"] = client_secret
        response = self.client.post(TOKEN_URL, params=token_params)
        return self._process_get_access_token(response)


class AuthorizationAsync(_BaseAuthorization):
    def __init__(self, client_id: str, redirect_uri: str):
        super().__init__(client_id, redirect_uri)
        self.client = AsyncClient(
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

    async def close(self):
        await self.client.aclose()

    async def authorization_request(
            self,
            response_type: Literal["code"] = "code",
            scope: list[str] = DEFAULT_SCOPE,
            instance_name: str | None = None
    ) -> str:
        auth_params = dict(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=" ".join(scope),
            response_type=response_type
        )
        if instance_name:
            auth_params["instance_name"] = instance_name

        response = await self.client.post(AUTH_URL, params=auth_params)
        return str(response.url)

    async def get_access_token(
            self,
            code: str,
            grant_type: Literal["authorization_code"] = "authorization_code",
            client_secret: str | None = None
    ) -> str | None:
        token_params = dict(
            code=code,
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            grant_type=grant_type
        )
        if client_secret:
            token_params["client_secret"] = client_secret
        response = await self.client.post(TOKEN_URL, params=token_params)
        return self._process_get_access_token(response)
