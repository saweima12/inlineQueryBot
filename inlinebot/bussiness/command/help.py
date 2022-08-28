from aiogram.types import Message
from inlinebot import textlang
from inlinebot.services import bot as _bot

async def show_help(*params, message: Message, **options):
    bot = _bot.get_bot()
    await bot.send_message(message.chat.id, textlang.HELP_MSG, parse_mode="markdown")