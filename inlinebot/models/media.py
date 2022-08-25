from typing import List
from inlinebot.extension.pydantic import OrjsonBaseModel

class MediaItem(OrjsonBaseModel):
    media_type: str
    unique_id: str
    file_id: str
    keywords: List[str]


class TelegramUser(OrjsonBaseModel):
    user_id: str
