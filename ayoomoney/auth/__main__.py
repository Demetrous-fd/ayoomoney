from ayoomoney import auth
import click


@click.group()
def main():
    pass


@main.command()
@click.argument("client_id")
@click.argument("redirect_url")
@click.option("--scope", default="", help="Список разрешений/scope, по умолчанию включены все разрешения")
def simple(client_id: str, redirect_url: str, scope: str):
    auth.simple.authorize(
        client_id,
        redirect_url,
        scope=scope.split(",") if scope else auth.simple.DEFAULT_SCOPE
    )


@main.command()
@click.argument("client_id")
@click.argument("redirect_url")
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=80, help="Порт приложения")
@click.option("--scope", default="", help="Список разрешений/scope, по умолчанию включены все разрешения")
def auto(client_id: str, redirect_url: str, host: str, port: int, scope: str):
    auth.auto.authorize(
        client_id,
        redirect_url,
        host=host,
        port=port,
        scope=scope.split(",") if scope else auth.auto.DEFAULT_SCOPE
    )


if __name__ == '__main__':
    main()
