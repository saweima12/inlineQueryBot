import os
from sanic import Sanic

from .services import bot, meili
from .entities import ConfigIndex, CheckedMediaIndex, UnCheckedMediaIndex
from . import config, views, handler


# define sanic application.
app = Sanic(__name__, env_prefix="INLINEBOT_")
# load default config
app.update_config(config)

# load config on environment path.
env_path = os.environ.get("INLINEBOT_CONFIG")
if env_path:
    app.update_config(env_path)

# register meilisearch index.
indexs_list = [
    ConfigIndex(),
    CheckedMediaIndex(),
    UnCheckedMediaIndex()
]

# setup search engine.
meili.setup(app, indexs_list)

# setup bot instance.
bot.setup(app)

# setup bussiness logic.
handler.register_handler(app)

# register route.
views.register(app)
