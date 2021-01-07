import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.utils.Utils as Utils
import src.commands.Command as Command
from src.commands.CommandReturn import CommandReturn, ErrorType

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

x = ":x:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Removes a shortcut (nickname).\n"
    msg += "`!!remove <shortcut>`\n"
    msg += "`shortcut`: The shortcut (nickname) to remove.\n\n"
    msg += "Example: `!!remove World`"
    return msg

async def handle(bot, command, message, arguments):
    # get the name of the shortcut to remove from the list of positional arguments
    name = arguments.get_pos(0)
    name = name.strip("\n")

    # if the shortcut does not exist, abort
    if not name in bot.shortcuts:
        error = "This shortcut (nickname) does not exist!\n"
        return CommandReturn(error + await usage(), None, ErrorType.ShortcutError)

    # remove the shortcut
    del bot.shortcuts[name]
    msg = "The shortcut (nickname) " + name + " has successfully been removed!\n"

    await Utils.save_shortcuts(bot)

    return CommandReturn(msg)

command = Command.Command()
command.name = "REMOVE"
command.emojis = [x]
command.activation = "!!remove"
command.usage = usage
command.handle = handle
command.expected_pos = 1