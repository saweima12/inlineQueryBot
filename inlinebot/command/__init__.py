from inlinebot.extension.command import CommandMap

from .register import register_user

command_map = CommandMap(prefix="/")
command_map.register_command_handler("register", register_user)