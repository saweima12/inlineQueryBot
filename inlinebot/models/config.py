from __future__ import annotations

from typing import List
from inlinebot.extension.pydantic import OrjsonBaseModel
from meilisearch_python_async import Client
from meilisearch_python_async.index import Index

from inlinebot.entities import ConfigIndex

class WhiteListConfig(OrjsonBaseModel):
    uid: str = "whitelist"
    users: List[str] = []

    @classmethod
    def get_index(cls, client: Client) -> Index:
        return client.index(ConfigIndex().uid)

    @classmethod
    async def get_config(cls , client: Client) -> 'WhiteListConfig' | None:
        # try get config from index
        try:
            # select index
            selected = cls.get_index(client)
            result = await selected.get_document(WhiteListConfig().uid)
            config = WhiteListConfig(**result)
            return config
        except:
            return None

    @classmethod
    async def add_user(cls, user_id: str, client: Client) -> None:
        config = await cls.get_config(client)
        users = set(config.users)

        if user_id in users:
            return 

        users.add(user_id)
        config.users = users
        # write into index
        selected = cls.get_index(client)
        selected.add_documents([config.dict()])
        

    @classmethod
    async def has_user(cls, user_id: str, client: Client) -> bool:
        config = await cls.get_config(client)
        users = set(config.users)
        if user_id in users:
            return True
        return False