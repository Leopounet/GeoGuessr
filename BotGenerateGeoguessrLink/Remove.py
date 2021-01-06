import time

import Utils
import Command

from CommandReturn import CommandReturn, ErrorType

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
    msg += "`shortcut`: The shortcut (nickname) to remove.\n"
    return msg

async def handle(bot, command, message, content):
    # url : name
    name = content[1]
    name = name.strip("\n")

    if not name in bot.shortcuts:
        error = "This shortcut (nickname) does not exist!\n"
        return CommandReturn(error + await usage(), None, ErrorType.ShortcutError)

    del bot.shortcuts[name]
    msg = "The shortcut (nickname) " + name + " has successfully been removed!\n"

    await Utils.saveShortcuts(bot)

    return CommandReturn(msg)

command = Command.Command()
command.name = "REMOVE"
command.emojis = [x]
command.activation = "!!remove"
command.nbArgs = [2]
command.usage = usage
command.handle = handle