from sanic import Sanic
from . import bot

def register(app: Sanic):
    app.blueprint(bot.bp)