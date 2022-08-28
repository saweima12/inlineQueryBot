from inlinebot.extension.command import CommandMap

from .register import register_user
from .keyword import add_keyword, set_keyword

command_map = CommandMap(prefix="/")
command_map.register_command_handler("register", register_user)
command_map.register_command_handler("sk", set_keyword)
command_map.register_command_handler("ak", add_keyword)