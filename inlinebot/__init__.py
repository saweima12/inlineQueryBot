import os
from sanic import Sanic
from inlinebot.services import bot
from inlinebot.view import bp

from . import config

# define sanic application.
app = Sanic(__name__, env_prefix="INLINEBOT_")
# load default config
app.update_config(config)

# load config on environment path.
env_path = os.environ.get("_INLINEBOT_CONFIG")
if env_path:
    app.update_config(env_path)


# register service.
bot.setup(app)

# register route.
app.static("/admin", "/static/admin")
app.blueprint(bp)
