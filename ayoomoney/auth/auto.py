from http.server import BaseHTTPRequestHandler
from contextlib import closing
import socketserver
import socket

from .base import Authorization, DEFAULT_SCOPE
from ayoomoney.errors import CreateTokenError

HOST = "127.0.0.1"
PORT = 80


def is_port_free(host, port) -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return False
        else:
            return True


class CodeHandler(BaseHTTPRequestHandler):
    client_id = None
    redirect_url = None
    auth_client: Authorization = None
    access_token: str | None = None

    def log_request(self, code: int | str = ..., size: int | str = ...) -> None:
        pass

    def do_GET(self):
        if "code=" not in self.path:
            self.send_response(400)
            self.end_headers()
            return

        code = self.path.split("code=")[-1]
        access_token = ""
        error = None

        try:
            access_token = self.auth_client.get_access_token(code)
        except CreateTokenError as e:
            error = e

        if error:
            print(error)
            body = f"""<div style="word-wrap: break-word;"><b>error:</b> {error}</div>"""
        else:
            body = f"""<div style="word-wrap: break-word;"><b>access_token:</b> {access_token}</div>"""

        print(f"{access_token=}")
        self.access_token = access_token
        self.send_response(200)
        self.send_header("charset", "windows-1251")
        self.end_headers()
        self.wfile.write(body.encode("windows-1251"))


def authorize(
        client_id: str,
        redirect_uri: str,
        scope: list[str] = DEFAULT_SCOPE,
        host: str = HOST, port: int = PORT,
        *_
) -> str | None:
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

    auth = Authorization(client_id, redirect_uri)
    url = auth.authorization_request(scope=scope)
    print("\n".join([
        "Перейдите по ссылке и подтвердите доступ для приложения:",
        url,
        "",
        "После подтверждения вы получите access_token, его можно скопировать с web-страницы или консоли.",
        f"Для отмены операции перейдите по адресу: http://{host}:{port}",
        ""
    ]))

    handler = CodeHandler
    handler.client_id = client_id
    handler.redirect_url = redirect_uri
    handler.auth_client = auth
    with socketserver.TCPServer((host, port), CodeHandler) as httpd:
        httpd.handle_request()

    return handler.access_token
