import asyncio
from typing import Tuple
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

    # check command is avaliable
    is_ok, msg = await is_avaliable(params, helper=helper, meili=meili) 
    if not is_ok:
        await helper.msg.reply(msg)
        return
  
    # log user command
    user_name = helper.msg.from_user.full_name
    command = helper.msg.text
    logger.info(f"[{user_name}] {command}")

    reply_helper = MessageHelper(helper.msg.reply_to_message)
    
    if not params:
        return

    # get first params & split.
    keywords = str(params[0]).split(',')

    # try get document from checked.
    content: Sticker | Animation = reply_helper.content
    item = await CheckedMediaItem.get_item(content.file_unique_id, meili)

    # overwirte checked item.
    if item:
        item.keywords = keywords
        await item.save(meili)
        await helper.msg.reply(textlang.SK_SUCCESS.format(keywords=item.keywords))
        return

    #  try get document from unchecked.
    item = await UnCheckedMediaItem.get_item(content.file_unique_id, meili)

    if not item:
        # didn't find document reply error
        await helper.msg.reply(textlang.SK_404_DOCUMENT)
        return
    
    checked_item = CheckedMediaItem(**item.dict())
    checked_item.keywords = keywords
    
    # remove from unchecked, insert into checked.
    await asyncio.gather(
        item.delete(meili),
        checked_item.save(meili)
        helper.msg.reply(textlang.SK_SUCCESS.format(keywords=checked_item.keywords))
    )


async def add_keyword(*params, helper: MessageHelper, **options):
    # check whitelist
    meili = get_client()

    is_ok, msg = await is_avaliable(params, helper=helper, meili=meili) 

    # check command is avaliable.
    if not is_ok:
        await helper.msg.reply(msg)
        return

    if not params:
        return
    
    # log user command
    user_name = helper.msg.from_user.full_name
    command = helper.msg.text
    logger.info(f"[{user_name}] {command}")
  
    reply_helper = MessageHelper(helper.msg.reply_to_message)
        
    # get first params & split.
    keywords = str(params[0]).split(',')

    # try get document from checked.
    content: Sticker | Animation = reply_helper.content
    item = await CheckedMediaItem.get_item(content.file_unique_id, meili)

    # overwirte checked item.
    if item:
        item.keywords = [*item.keywords, *keywords]
        await item.save(meili)
        await helper.msg.reply(textlang.AK_SUCCESS.format(keywords=item.keywords))
        return

    #  try get document from unchecked.
    item = await UnCheckedMediaItem.get_item(content.file_unique_id, meili)

    # didn't find document reply error
    if not item:
        await helper.msg.reply(textlang.SK_404_DOCUMENT)
        return

    # remove from unchecked, insert into checked.
    checked_item = CheckedMediaItem(**item.dict())
    checked_item.keywords = keywords
    
    # save to checked db.
    await asyncio.gather(
        item.delete(meili),
        checked_item.save(meili)
        helper.msg.reply(textlang.AK_SUCCESS.format(keywords=checked_item.keywords))
    )

    
async def remove_media(*params, helper: MessageHelper, **options):
    # check whitelist
    meili = get_client()

    is_ok, msg = await is_avaliable(params, helper=helper, meili=meili) 

    # check command is avaliable.
    if not is_ok:
        await helper.msg.reply(msg)
        return

    # log user command
    user_name = helper.msg.from_user.full_name
    command = helper.msg.text
    logger.info(f"[{user_name}] {command}")

    reply_helper = MessageHelper(helper.msg.reply_to_message)
    # try get document from checked.
    content: Sticker | Animation = reply_helper.content
    item = await CheckedMediaItem.get_item(content.file_unique_id, meili)
    
    # didn't find document reply error
    if not item:
        await helper.msg.reply(textlang.SK_404_DOCUMENT)
        return

    # remove item & send reply message.
    await asyncio.gather(
        item.delete(meili),
        helper.msg.reply(textlang.RM_SUCCESS)
    )



async def is_avaliable(*params, helper: MessageHelper, meili: Client) -> Tuple[bool, str]:
 
    has_user = await WhiteListConfig.has_user(helper.user_id, meili)
    if not has_user:
        return False

    # check reply message.
    reply_msg = helper.msg.reply_to_message
    if not reply_msg:
        return (False, textlang.SK_NEED_REPLY)
    
    reply_helper = MessageHelper(reply_msg)
    if not reply_helper.is_media():
        return (False, textlang.SK_NEED_REPLY)

    # check params
    if len(params) < 1:
        return (False, textlang.SK_PRAMAS_ERROR)

    return (True, "")