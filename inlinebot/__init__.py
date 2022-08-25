import os
from sanic import Sanic
from inlinebot.services import bot, search
from inlinebot.services.search.types import MeiliIndex

from . import config, views, handler


# define sanic application.
app = Sanic(__name__, env_prefix="INLINEBOT_")
# load default config
app.update_config(config)

# load config on environment path.
env_path = os.environ.get("INLINEBOT_CONFIG")
if env_path:
    app.update_config(env_path)


indexs_list = [
    MeiliIndex("config", "id"), 
    MeiliIndex("checked", "uid"), 
    MeiliIndex("unchecked", "uid")
]

# setup search engine.
search.setup(app, indexs_list)

# setup bot instance.
bot.setup(app)

# setup bussiness logic.
handler.register_handler(app)

# register route.
views.register(app)
app.static("/admin", "static/admin")