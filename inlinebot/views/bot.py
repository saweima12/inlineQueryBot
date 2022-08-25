from sanic import Blueprint, Request, response
from sanic.log import logger
from aiogram.types import Update
from inlinebot.services import bot

bp = Blueprint("inline_query")

@bp.post("/<token:str>")
async def on_update(request: Request, token: str):
    
    # get bot & dp
    _bot = bot.get_bot()
    _dp = bot.get_dp()

    if token != _bot._token:
        return response.empty(200)

    update = Update(**request.json)
    logger.debug(f"on_update {update.as_json()}")
    # set default bot & dispatch event.
    _bot.set_current(_bot)
    await _dp.process_update(update)

    return response.empty(200)
