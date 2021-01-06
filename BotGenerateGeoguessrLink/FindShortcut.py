import time
import Command

from CommandReturn import CommandReturn, ErrorType

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
    msg += "`url`: URL to the map.\n"
    return msg

async def handle(bot, command, message, content):
    url = content[1]
    msg = ""

    for shortcut in bot.shortcuts:
        if bot.shortcuts[shortcut]["url"][:-1] == url:
            msg = "Map: `" + bot.shortcuts[shortcut]["title"] + "` -> Alias: `" + shortcut + "`"

    if msg == "":
        msg = "This URL has no nickname (shortcut) yet, you can add it by using `!!add`."

    return CommandReturn(msg)

command = Command.Command()
command.name = "FIND"
command.emojis = [question]
command.activation = "!!find"
command.nbArgs = [2]
command.usage = usage
command.handle = handle