import time
import Command

from CommandReturn import CommandReturn, ErrorType

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use (help)
book = ":book:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Affiche tous les shortcuts disponibles.\n"
    msg += "`!!list`\n"
    return msg

async def handle(bot, command, message, content):
    msg = ""

    for shortcut in bot.shortcuts:
        msg += "Map: `" + bot.shortcuts[shortcut]["title"] + "` -> Alias: `" + shortcut + "`\n"

    if msg == "":
        msg = "Aucun shortcut n'a été ajouté pour l'instant!"

    return CommandReturn(msg)

command = Command.Command()
command.name = "LIST"
command.emojis = [book]
command.activation = "!!list"
command.nbArgs = [1]
command.usage = usage
command.handle = handle