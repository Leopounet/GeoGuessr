import time
import Command

from CommandReturn import CommandReturn, ErrorType

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use (help)
thumbsup = ":thumbsup:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Prints this help.\n"
    msg += "`!!help`\n"
    return msg

async def handle(bot, command, message, content):
    return CommandReturn("", bot.help)

command = Command.Command()
command.name = "HELP"
command.emojis = [thumbsup]
command.activation = "!!help"
command.nbArgs = [1]
command.usage = usage
command.handle = handle