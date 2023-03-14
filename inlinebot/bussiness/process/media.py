from re import I
from typing import Tuple

from sanic.config import Config
from aiogram.types import (
    Sticker,
    Animation,
    Audio,
    InlineQueryResultCachedMpeg4Gif,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedAudio
)
from inlinebot.extension.helper import MessageHelper
from meilisearch_python_async import Client

from inlinebot.models import UnCheckedMediaItem


def get_search_tuple(query: str) -> Tuple[str, str]:
    keywords = query.split(":")
    if len(keywords) >= 2:
        return keywords[0], keywords[1]
    return "", query

def get_inline_media(uid: str, media_type: str, file_id: str, search_type: str):

    if search_type == "mp3":
        if media_type == "audio":
            return InlineQueryResultCachedAudio(id=uid, audio_file_id=file_id)
    else:
        if media_type == "sticker":
            return InlineQueryResultCachedSticker(id=uid, sticker_file_id=file_id)
        elif media_type == "animation":
            return InlineQueryResultCachedMpeg4Gif(id=uid, mpeg4_file_id=file_id)



async def add_media(helper: MessageHelper, client: Client, config: Config):

    content: Sticker | Animation | Audio = helper.content
    # get file params
    uid = content.file_unique_id
    cache_dir = config.get("CACHE_DIR", "./static/asset")
    domain_url = config.get("DOMAIN_URL")
    cache_root_url = config.get("CACHE_ROOT_URL")
    # create media item.
    item = UnCheckedMediaItem(uid=uid, 
                        media_type=helper.content_type, 
                        file_id=helper.content["file_id"])    
    
    # process save_path
    save_path = get_media_savepath(helper)
    item.file_path = save_path

    # save thumb
    if content.thumb:
        await content.thumb.download(destination_file=f"{cache_dir}/{save_path}")
    else:
        await content.download(destination_file=f"{cache_dir}/{save_path}")

    # generate cache_url
    if cache_root_url:
        item.cache_url = f"{cache_root_url}/{save_path}"
    else:
        item.cache_url = f"{domain_url}/asset/{save_path}"

    # save image.
    await item.save(client)

def get_media_savepath(helper: MessageHelper) -> str:
    # generate save_path
    content = helper.content

    if helper.is_sticker():
        return f"{content.set_name}/{content.file_unique_id}.webp"

    if helper.is_animation():
        if content.thumb:
            return f"gif/{content.file_unique_id}.webp"
    
        # check media_type
        if content.mime_type == "video/mp4":
            return f"gif/{content.file_unique_id}.mp4"

    if helper.is_audio():
        return f"audio/{content.file_unique_id}.mp4"