from __future__ import annotations
from typing import Any, Dict, List
from inlinebot.extension.pydantic import OrjsonBaseModel

from meilisearch_python_async import Client
from meilisearch_python_async.index import Index

from inlinebot.entities import CheckedMediaIndex


class CheckedMediaItem(OrjsonBaseModel):
    uid: str
    media_type: str
    file_id: str
    keywords: List[str] = []
    attach: Dict[str, Any] = {}
    cache_url: str = ""
    file_path: str = ""


    @classmethod
    def get_index(cls, client: Client) -> Index:
        return client.index(CheckedMediaIndex().uid)
 

    @classmethod
    async def get_items(cls, client:Client, limit=300) -> List['CheckedMediaItem'] | None:
        selected = cls.get_index(client)
        response = await selected.get_documents(limit=limit)
        items = [ cls(**item) for item in response.result ]
        return items
    
    @classmethod
    async def get_item(cls, uid: str, client: Client) -> 'CheckedMediaItem' | None:
        selected = cls.get_index(client)
        try:
            result = await selected.get_document(uid)
            item = cls(**result)
            return item
        except:
            return None

    async def save(self, client:Client) -> None:
        selected = self.get_index(client)
        await selected.add_documents([self.dict()])

    async def delete(self, client: Client) -> None:
        selected = self.get_index(client)
        await selected.delete_document(self.uid)
    