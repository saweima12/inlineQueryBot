from typing import List
from inlinebot.extension.pydantic import OrjsonBaseModel

class WhiteUserList(OrjsonBaseModel):
    list: List[str]
