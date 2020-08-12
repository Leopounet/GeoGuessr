import time
import Command

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use (help)
thumbsup = ":thumbsup:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Affiche cette aide.\n"
    msg += "`!!help`\n"
    return msg

async def handle(bot, command, message, content):
    return "", bot.help

command = Command.Command()
command.name = "HELP"
command.emojis = [thumbsup]
command.activation = "!!help"
command.nbArgs = [1]
command.usage = usage
command.handle = handle