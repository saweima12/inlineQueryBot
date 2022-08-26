from aiogram.types import Message, ContentTypes

class MessageHelper:

    def __init__(self, message: Message):
        self.msg = message

    @property
    def content_type(self):
        return str(self.msg.content_type)

    @property
    def content(self):
        return self.msg.to_python().get(self.content_type)

    def is_media(self):
        return self.content_type in ["sticker", "animation"]

    def is_text(self):
        return self.msg.content_type == "text"
    
    def is_sticker(self):
        return self.msg.content_type == "sticker"
    
    