import time

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Retourne l'alias lié à cet URL (si existant).\n"
    msg += "`!!find <url>`\n"
    msg += "`url`: URL de la map.\n"
    return msg

async def handleFind(bot, message):
    if len(message.content.split(" ")) != 2:
        error = "Nombre d'argument invalide!\n"
        return error + await usage()

    url = message.content.split(" ")[1]

    for shortcut in bot.shortcuts:
        if bot.shortcuts[shortcut]["url"] == url:
            return "Map: `" + bot.shortcuts[shortcut]["title"] + "` -> Alias: `" + shortcut + "`"

    return "Cette map n'a pas encore été ajoutée, il est possible de l'jaouter avec la commande `!!add`."