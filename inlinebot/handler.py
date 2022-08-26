from typing import Dict
from sanic import Sanic
from aiogram.types import Message, ContentTypes, InlineQuery

from .models.config import WhiteListConfig
from .models.unchecked import UnCheckedMediaItem

from .services import bot, meili
from .command import command_map
from .helper import MessageHelper



def register_handler(app: Sanic):
    # get bot 
    dp = bot.get_dp()
    client = meili.get_client()

    @dp.message_handler(content_types=ContentTypes.ANY)
    async def on_message(message: Message):
        
        helper = MessageHelper(message)

        if helper.is_text():
            if command_map.is_avaliable(message.text):
                await command_map.notify(message.text, message=message)

        print(helper.content_type)
        if not helper.is_media():
            return

        user_id = str(message.from_user.id)
        has_user = await WhiteListConfig.has_user(user_id, client)

        # check permission
        if not has_user:
            return
        
        # write content into meili
        content : Dict[str,any] = helper.content 
        item = UnCheckedMediaItem(uid=content["file_unique_id"], 
                                media_type=helper.content_type, 
                                file_id=content["file_id"])

        if helper.is_sticker():
            print("is_sticker")
        



    @dp.inline_handler()
    async def on_inline(message: InlineQuery):
        pass
        