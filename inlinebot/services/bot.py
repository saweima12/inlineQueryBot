from aiogram import Bot, Dispatcher
from sanic import Sanic

def get_bot() -> Bot:
    pass

def get_dp(app: Sanic) -> Dispatcher:
    pass

def setup(app: Sanic):
    bot_token = app.config["BOT_TOKEN"]
    
    bot = Bot(token=bot_token)
    dispatcher = 


