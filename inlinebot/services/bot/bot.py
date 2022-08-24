from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentTypes
from sanic import Sanic

SERVICE_CODE = "bot"
DP_CODE = f"{SERVICE_CODE}_dp" 


def get_bot() -> Bot:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)

def get_dp() -> Dispatcher:
    app = Sanic.get_app()
    return getattr(app.ctx, DP_CODE)

def setup(app: Sanic):
    token = app.config["BOT_TOKEN"]
    webhook_url = app.config["DOMAIN_URL"]

    bot = Bot(token)
    dp = Dispatcher(bot)

    @dp.message_handler(content_types=ContentTypes.ANY)
    async def on_message(message: Message):
        await message.reply("Hello")
    
    @app.main_process_start
    async def startup(app: Sanic):
        await bot.set_webhook(webhook_url)

    @app.before_server_stop
    async def dispose(app: Sanic):
        await bot.delete_webhook()

    setattr(app.ctx, SERVICE_CODE, bot)
    setattr(app.ctx, DP_CODE, dp)


