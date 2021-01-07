import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.commands.Command as Command
from src.commands.CommandReturn import CommandReturn, ErrorType

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use (help)
question = ":question:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Prints the name of the shortcut bound to this map (if it exists).\n"
    msg += "`!!find <url>`\n"
    msg += "`url`: URL to the map.\n\n"
    msg += "Example: `!!find https://www.geoguessr.com/maps/world`"
    return msg

async def handle(bot, command, message, arguments):

    # get the url from the first positional argument
    url = arguments.get_pos(0)

    # the message to eventually return
    msg = ""

    # reads all the shortcuts possible
    for shortcut in bot.shortcuts:

        # if the shortcut has been found add it to the message
        if bot.shortcuts[shortcut]["url"].strip("\n") == url:
            msg = "Map: `" + bot.shortcuts[shortcut]["title"] + "` -> Alias: `" + shortcut + "`"
            break

    # if the message is empty, then the shortcut was not set in the first place
    if msg == "":
        msg = "This URL has no nickname (shortcut) yet, you can add it by using `!!add`."

    return CommandReturn(msg)

command = Command.Command()
command.name = "FIND"
command.emojis = [question]
command.activation = "!!find"
command.usage = usage
command.handle = handle
command.expected_pos = 1