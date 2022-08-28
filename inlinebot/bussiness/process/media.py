from re import I
from sanic.config import Config
from aiogram.types import Sticker, Animation 
from inlinebot.extension.helper import MessageHelper
from meilisearch_python_async import Client

from inlinebot.models import UnCheckedMediaItem, CheckedMediaItem

async def add_media(helper: MessageHelper, client: Client, config: Config):
    content: Sticker | Animation = helper.content
    # get file params
    uid = content.file_unique_id
    cache_dir = config.get("CACHE_DIR", "./static/asset")
    domain_url = config.get("DOMAIN_URL")
    cache_root_url = config.get("CACHE_ROOT_URL")
    # create media item.
    item = UnCheckedMediaItem(uid=uid, 
                        media_type=helper.content_type, 
                        file_id=helper.content["file_id"])    
    
    # generate save_path
    if helper.is_sticker():
        save_path = f"{content.set_name}/{content.file_unique_id}.webp"
    elif helper.is_animation():
        save_path = f"gif/{content.file_unique_id}.webp"

    item.file_path = save_path
    # save thumb
    await content.thumb.download(destination_file=f"{cache_dir}/{save_path}")
    
    # generate cache_url
    if cache_root_url:
        item.cache_url = f"{cache_root_url}/{save_path}"
    else:
        item.cache_url = f"{domain_url}/asset/{save_path}"

    # save image.
    await item.save(client)
