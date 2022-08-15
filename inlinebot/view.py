from sanic import Blueprint, Request

from .services import bot

bp = Blueprint()

@bp.post('/mmbq/<token:str>')
async def on_update(request: Request, token: str):
    
    _bot = bot.get_bot()

