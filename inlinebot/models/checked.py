from __future__ import annotations
from typing import Any, Dict, List
from inlinebot.extension.pydantic import OrjsonBaseModel

class CheckedMediaItem(OrjsonBaseModel):
    uid: str
    media_type: str
    file_id: str
    keywords: List[str]
    attach: Dict[str, Any]