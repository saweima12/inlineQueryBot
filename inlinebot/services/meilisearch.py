from sanic import Sanic
from meilisearch.client import Client


def get_client() -> Client:
    app = Sanic.get_app()

    _api_url = app.config[""]


    return Client()


def setup(app: Sanic):
    pass

