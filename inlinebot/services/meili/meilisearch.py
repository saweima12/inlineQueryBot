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

    # set lifecycle hook
    @app.main_process_start
    async def on_main_startup(app: Sanic):
        # print all keys.
        keys = await client.get_keys()
        for key in keys.results:
            print(f"{key.name}:", key.key)

        for item in index_list:
            await client.create_index(item.uid, item.primary_key)
            if item.setting:
                await client.index(item.uid).update_settings(item.setting)
    

    @app.before_server_stop
    async def before_stop(app: Sanic):
        await client.aclose()

    # attach to ctx
    setattr(app.ctx, SERVICE_CODE, client)
