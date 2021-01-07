import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.commands.Command as Command

from src.commands.CommandReturn import CommandReturn

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use (help)
book = ":book:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Displays all the available nicknames (shortcuts).\n"
    msg += "`!!list`\n\n"
    msg += "Example: `!!list`"
    return msg

async def handle(bot, command, message, arguments):
    msg = ""

    for shortcut in bot.shortcuts:
        msg += "Map: `" + bot.shortcuts[shortcut]["title"] + "` -> Alias: `" + shortcut + "`\n"

    if msg == "":
        msg = "No shortcut (nickname) has been added yet!"

    return CommandReturn(msg)

command = Command.Command()
command.name = "LIST"
command.emojis = [book]
command.activation = "!!list"
command.usage = usage
command.handle = handle

command.expected_pos = 0