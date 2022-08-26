from sanic import Sanic
from sanic.log import logger
from aiogram.types import Message
from inlinebot.models import WhiteListConfig
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


    client = get_client()
    # get user_id
    user_id = str(message.from_user.id)
    await WhiteListConfig.add_user(user_id, client)
    logger.info(f"on register user: {user_id}")