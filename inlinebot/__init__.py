import os
from sanic import Sanic
from inlinebot.services import bot

from . import config, views

# define sanic application.
app = Sanic(__name__, env_prefix="INLINEBOT_")
# load default config
app.update_config(config)

# load config on environment path.
env_path = os.environ.get("INLINEBOT_CONFIG")
if env_path:
    app.update_config(env_path)


# register service.
bot.setup(app)

# register route.
views.register(app)
app.static("/admin", "static/admin")