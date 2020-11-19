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
    msg = "Retourne l'alias lié à cet URL (si existant).\n"
    msg += "`!!find <url>`\n"
    msg += "`url`: URL de la map.\n"
    return msg

async def handle(bot, command, message, content):
    url = content[1]
    msg = ""

    for shortcut in bot.shortcuts:
        if bot.shortcuts[shortcut]["url"][:-1] == url:
            msg = "Map: `" + bot.shortcuts[shortcut]["title"] + "` -> Alias: `" + shortcut + "`"

    if msg == "":
        msg = "Cette map n'a pas encore été ajoutée, il est possible de l'jaouter avec la commande `!!add`."

    return CommandReturn(msg)

command = Command.Command()
command.name = "FIND"
command.emojis = [question]
command.activation = "!!find"
command.nbArgs = [2]
command.usage = usage
command.handle = handle