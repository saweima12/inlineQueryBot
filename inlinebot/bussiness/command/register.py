from sanic import Sanic
from sanic.log import logger
from aiogram.types import Message
from inlinebot import textlang
from inlinebot.models import WhiteListConfig
from inlinebot.services.bot import get_bot
from inlinebot.services.meili import get_client

async def register_user(*params, message: Message, **options):
    # get authencitcate params
    REGISTER_KEY = Sanic.get_app().config.get("REGISTRY_KEY", "")
    if len(params) != 1:
        return

    # validate authenticate_key
    authenticate_key = params[0]
    if authenticate_key != REGISTER_KEY:
        return

    bot = get_bot()
    meili = get_client()
    # get user_id
    user_id = str(message.from_user.id)
    await WhiteListConfig.add_user(user_id, meili)
    logger.info(f"on register user: {user_id}")
    await message.reply(textlang.REGISTER_SUCCESS)
    await bot.send_message(message.chat.id, textlang.HELP_MSG)