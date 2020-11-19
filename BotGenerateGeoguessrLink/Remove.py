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
    msg = "Retire un raccourci.\n"
    msg += "`!!remove <shortcut>`\n"
    msg += "`shortcut`: Le shortcut à retirer.\n"
    return msg

async def handle(bot, command, message, content):
    # url : name
    name = content[1]
    name = name.strip("\n")

    if not name in bot.shortcuts:
        error = "Le shortcut n'existe pas!\n"
        return CommandReturn(error + await usage(), None, ErrorType.ShortcutError)

    del bot.shortcuts[name]
    msg = "Le raccourci " + name + " a été supprimé!\n"

    await Utils.saveShortcuts(bot)

    return CommandReturn(msg)

command = Command.Command()
command.name = "REMOVE"
command.emojis = [x]
command.activation = "!!remove"
command.nbArgs = [2]
command.usage = usage
command.handle = handle