import time
import Command

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

async def handle(bot, command, content):
    url = content[1]

    for shortcut in bot.shortcuts:
        if bot.shortcuts[shortcut]["url"] == url:
            return "Map: `" + bot.shortcuts[shortcut]["title"] + "` -> Alias: `" + shortcut + "`", None

    return "Cette map n'a pas encore été ajoutée, il est possible de l'jaouter avec la commande `!!add`.", None

command = Command.Command()
command.emojis = [question]
command.activation = "!!find"
command.nbArgs = [2]
command.usage = usage
command.handle = handle