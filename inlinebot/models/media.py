from typing import List
from inlinebot.extension import pydantic

class MediaItem(pydantic.OrjsonBaseModel):
    media_type: str
    unique_id: str
    file_id: str
    keywords: List[str]
