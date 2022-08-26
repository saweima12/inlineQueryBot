from __future__ import annotations
from meilisearch_python_async import Client
from meilisearch_python_async.index import Index

from typing import Any, Dict, List
from inlinebot.extension.pydantic import OrjsonBaseModel
from inlinebot.entities.indexs import UnCheckedMediaIndex

class UnCheckedMediaItem(OrjsonBaseModel):
    uid: str
    media_type: str
    file_id: str
    keywords: List[str] = []
    attach: Dict[str, Any] = {}

    @classmethod
    def get_index(cls, client: Client) -> Index:
        return client.index(UnCheckedMediaIndex().uid)
    
    @classmethod
    async def get_items(cls, client:Client) -> List['UnCheckedMediaItem'] | None:
        selected = cls.get_index(client)
        response = await selected.get_documents(limit=300)
        items = [ cls(**item) for item in response.result ]
        return items
    
    async def get_item(cls, uid: str, client: Client) -> 'UnCheckedMediaItem' | None:
        selected = cls.get_index(client)
        try:
            result = await selected.get_document(uid)
            item = cls(**result)
            return item
        except:
            return None

    async def save(self, client:Client) -> List['UnCheckedMediaItem'] | None:
        selected = self.get_index(client)
        await selected.add_documents([self.dict()])
        
    