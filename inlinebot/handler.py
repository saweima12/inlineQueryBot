from typing import Dict
from sanic import Sanic
from aiogram.types import Message, ContentTypes, InlineQuery, InlineQueryResultCachedSticker, InlineQueryResultCachedMpeg4Gif

from .services import bot, meili
from .models import CheckedMediaItem, UnCheckedMediaItem, WhiteListConfig
from .extension.helper import MessageHelper

from .bussiness.process.media import add_media
from .bussiness.command import command_map


def register_handler(app: Sanic):
    # get bot 
    dp = bot.get_dp()
    client = meili.get_client()
    @dp.message_handler(content_types=ContentTypes.ANY)
    async def on_message(message: Message):
        
        helper = MessageHelper(message)
        # process command
        if helper.is_text():
            if command_map.is_avaliable(message.text):
                await command_map.notify(message.text, message=message, helper=helper)
                return

        # check content is sticker or animation
        if not helper.is_media():
            return

        # check permission
        is_user = await WhiteListConfig.has_user(helper.user_id, client)
        if not is_user:
            return

        # check document not exists.
        uid = helper.content["file_unique_id"]

        # in checked return
        checked_item = await CheckedMediaItem.get_item(uid, client)
        if checked_item:
            return

        # in unchecked return.
        uncheced_item = await UnCheckedMediaItem.get_item(uid, client)
        if uncheced_item: 
            return

        # file is not exists, insert it.
        await add_media(helper, meili, app.config)


    @dp.inline_handler()
    async def on_inline(message: InlineQuery):
        pass
        # try:
        #   search by meilisearch
        #   generate inlineQueryResultCache
        #   pass
        # except Exception as _e:
        #     pass

        # # create answer

        # sticker1 = InlineQueryResultCachedSticker(
        #     id="1", sticker_file_id="CAACAgUAAxkBAANeYwiUinVTiYqnzFsrlJsq7d42gKgAAr8GAAJzKhFWWYdR2ZI-XyMpBA"
        # )
        # sticker2 = InlineQueryResultCachedMpeg4Gif(
        #     id="2", mpeg4_file_id="CgACAgUAAxkBAAOFYwnifGDyXRoPf5Q1lPpFR6E-n8kAArsGAAIDN3hWMVVnkLckNOApBA")
        
        # await message.answer([sticker1, sticker2])