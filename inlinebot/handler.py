import re
from sanic import Sanic
from sanic.log import logger
from aiogram.types import (
    Message, 
    ContentTypes, 
    InlineQuery
)

from inlinebot import textlang

from .services import bot, meili
from .models import CheckedMediaItem, UnCheckedMediaItem, WhiteListConfig
from .extension.helper import MessageHelper

from .bussiness.process.media import add_media, get_inline_media, get_search_tuple
from .bussiness.command import command_map


def register_handler(app: Sanic):
    # get bot 
    dp = bot.get_dp()
    client = meili.get_client()

    @dp.message_handler(content_types=ContentTypes.ANY)
    async def on_message(message: Message):
        
        helper = MessageHelper(message)

        try:
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
                rtn_msg = textlang.MEDIA_CHECKED.format(keywords=checked_item.keywords)
                await message.reply(rtn_msg)
                return

            # in unchecked return.
            uncheced_item = await UnCheckedMediaItem.get_item(uid, client)
            if uncheced_item: 
                rtn_msg = textlang.MEDIA_UNCHECKED.format(keywords=uncheced_item.keywords)
                await message.reply(rtn_msg)
                return

            # file is not exists, insert it.
            rtn_msg = textlang.MEDIA_NEW
            await message.reply(rtn_msg)
            await add_media(helper, client, app.config)
        except Exception as _e:
            logger.error(_e.args)
            logger.error(f"Error: {message.as_json()}")
            await message.reply(textlang.MSG_500)


    @dp.inline_handler()
    async def on_inline(message: InlineQuery):
        try:
            query_str = message.query
            search_type, keywords = get_search_tuple(query_str)
            logger.debug(f"Search: {search_type}, {keywords}")

            result = await client.index("checked").search(keywords)
            cache_time = app.config.get("INLINE_CACHE_TIME", 180)

            # declare answer list.
            answers = []
            for item in result.hits:
                # get params
                uid = item.get("uid")
                media_type = item.get("media_type")
                file_id = item.get("file_id")
                # create result item.
                media = get_inline_media(uid, media_type, file_id, search_type)
                if media:
                    answers.append(media)
            # return anser
            logger.info(f"Query [{message.from_user.full_name}] {message.query}")
            await message.answer(answers, cache_time=cache_time)
        except Exception as _e:
            logger.error(_e)