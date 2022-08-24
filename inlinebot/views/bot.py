from sanic import Blueprint, Request, response
from aiogram.types import Update
from inlinebot.services import bot

bp = Blueprint("inline_query", url_prefix="/mmbq")

@bp.post("/<token:str>")
async def on_update(request: Request, token: str):
    
    # get bot & dp
    _bot = bot.get_bot()
    _dp = bot.get_dp()

    if token != _bot._token:
        return response.empty(200)

    update = Update(**request.json)

    # set default bot & dispatch event.
    _bot.set_current(_bot)
    _dp.process_update(update)
