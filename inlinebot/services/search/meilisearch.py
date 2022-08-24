from typing import List
from sanic import Sanic
from meilisearch_python_async import Client

from .types import MeiliIndex

SERVICE_CODE = "meilisearch"

def get_client() -> Client:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)


def setup(app: Sanic, index_list: List[MeiliIndex]=[]):
    meili_url = app.config.get("MEILISEARCH_URL")
    meili_key = app.config.get("MEILISEARCH_MASTERKEY")
    client = Client(meili_url,meili_key)

    # initialize 
    async def on_main_startup():
        for item in index_list:
            await client.create_index(item.uid, item.primary_key)


    async def before_stop():
        await client.aclose()

    # attach to ctx
    setattr(app.ctx, SERVICE_CODE, client)
