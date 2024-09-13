from http.server import BaseHTTPRequestHandler
from contextlib import closing
import socketserver
import socket

import httpx

HOST = "127.0.0.1"
PORT = 80
DEFAULT_SCOPE = (
    "account-info",
    "operation-history",
    "operation-details",
    "incoming-transfers",
    "payment-p2p",
    "payment-shop",
)


def is_port_free(host, port) -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return False
        else:
            return True


class CodeHandler(BaseHTTPRequestHandler):
    client_id = None
    redirect_url = None

    def log_request(self, code: int | str = ..., size: int | str = ...) -> None:
        pass

    def do_GET(self):
        if "code=" not in self.path:
            self.send_response(400)
            self.end_headers()
            return

        code = self.path.split("code=")[-1]
        token_params = dict(
            code=code,
            client_id=self.client_id,
            redirect_uri=self.redirect_url,
            grant_type="authorization_code"
        )
        response = httpx.post("https://yoomoney.ru/oauth/token", params=token_params)

        data = response.json()
        access_token = data.get("access_token")

        print(f"{access_token=}")
        body = f"""<div style="word-wrap: break-word;"><b>access_token:</b> {access_token}</div>"""
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body.encode())


def authorize(
        client_id: str,
        redirect_uri: str,
        app_permissions: list[str] = DEFAULT_SCOPE,
        host: str = HOST, port: int = PORT,
        *_
):
    if not is_port_free(host, port):
        print(
            f"Порт: {port} занят другим приложением. "
            f"Попробуйте закрыть его или укажите другой порт командой: `--port N`\n"
        )
        print(
            "После изменения порта нужно изменить redirect_uri приложения, зайдите на страницу: "
            "https://yoomoney.ru/settings/oauth-services"
        )
        print("и в поле redirect_uri добавьте текущий порт: http://my.localhost:N")
        exit(1)

    parts = redirect_uri.split(":")
    if len(parts) > 2:
        _port = int(parts[-1])
        if _port != port:
            print(
                f"Порт в {redirect_uri=} не совпадает с текущим: {port}. "
                f"Укажите порт {_port} командой: `--port {_port}`"
            )
            exit(1)

    auth_params = dict(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=" ".join(app_permissions),
        response_type="code"
    )
    response = httpx.post("https://yoomoney.ru/oauth/authorize", params=auth_params)
    print("\n".join([
        "Перейдите по ссылке и подтвердите доступ для приложения:",
        str(response.url),
        "",
        "После подтверждения вы получите access_token, его можно скопировать с web-страницы или консоли.",
        f"Для отмены операции перейдите по адресу: http://{host}:{port}",
        ""
    ]))

    handler = CodeHandler
    handler.client_id = client_id
    handler.redirect_url = redirect_uri
    with socketserver.TCPServer((host, port), CodeHandler) as httpd:
        httpd.handle_request()
