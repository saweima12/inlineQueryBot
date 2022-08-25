from sanic import Sanic
from aiogram.types import Message, ContentTypes, InlineQuery

from inlinebot.services import bot, search
from inlinebot.command import command_map

def register_handler(app: Sanic):
    # get bot 
    dp = bot.get_dp()
        
    @dp.message_handler(content_types=ContentTypes.ANY)
    async def on_message(message: Message):
        
        print(message)

    @dp.inline_handler()
    async def on_inline(message: InlineQuery):
        pass
        