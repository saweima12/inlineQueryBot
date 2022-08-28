import asyncio
from sanic.log import logger
from aiogram.types import Message, Sticker, Animation
from meilisearch_python_async import Client

from inlinebot.extension.helper import MessageHelper
from inlinebot.models import WhiteListConfig, UnCheckedMediaItem, CheckedMediaItem
from inlinebot.services.meili import get_client
from inlinebot import textlang

async def set_keyword(*params, helper: MessageHelper, **options):
    
    # check whitelist
    meili = get_client()

    if not is_avaliable(params, helper, meili):
        return
  
    reply_helper = MessageHelper(helper.msg.reply_to_message)
        
    # get first params & split.
    keywords = str(params[0]).split(',')

    # try get document from checked.
    content: Sticker | Animation = reply_helper.content
    item = await CheckedMediaItem.get_item(content.file_unique_id, meili)

    # overwirte checked item.
    if item:
        item.keywords = keywords
        await item.save(meili)
        return

    #  try get document from unchecked.
    item = await UnCheckedMediaItem.get_item(content.file_unique_id, meili)

    if item:
        # remove from unchecked, insert into checked.
        checked_item = CheckedMediaItem(**item.dict())
        checked_item.keywords = keywords
        
        await asyncio.gather(
            item.delete(meili),
            checked_item.save(meili)
        )
        # save to checked db.
        return

    # didn't find document reply error
    await helper.msg.reply(textlang.SK_404_DOCUMENT)

async def add_keyword(*params, helper: MessageHelper, **options):
    pass

async def is_avaliable(*params, helper: MessageHelper, meili: Client):
 
    has_user = await WhiteListConfig.has_user(helper.user_id, meili)
    if not has_user:
        return False

    # check reply message.
    reply_msg = helper.msg.reply_to_message
    if not reply_msg:
        await helper.msg.reply(textlang.SK_NEED_REPLY)
        return False
    
    reply_helper = MessageHelper(reply_msg)
    if not reply_helper.is_media():
        await helper.msg.reply(textlang.SK_NEED_REPLY)
        return False

    # check params
    if len(params) < 1:
        await helper.msg.reply(textlang.SK_PRAMAS_ERROR)
        return False

    return True