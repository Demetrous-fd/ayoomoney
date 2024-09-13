from ayoomoney import auth
import click


@click.group()
def main():
    pass


@main.command()
@click.argument("client_id")
@click.argument("redirect_url")
def simple(client_id: str, redirect_url: str):
    auth.simple.authorize(client_id, redirect_url)


@main.command()
@click.argument("client_id")
@click.argument("redirect_url")
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=80, help="Порт приложения")
def auto(client_id: str, redirect_url: str, host: str, port: int):
    auth.auto.authorize(client_id, redirect_url, host=host, port=port)


if __name__ == '__main__':
    main()
