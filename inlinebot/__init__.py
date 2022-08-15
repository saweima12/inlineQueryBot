from sanic import Sanic, Request
from aiogram.types import Message

from inlinebot.services import bot
from inlinebot.view import bp

# define sanic application.
app = Sanic(__name__)



# register service.
bot.setup(app)


# initialize project
@app.main_process_start
async def main_startup():
    pass


# register route.
app.blueprint(bp)
