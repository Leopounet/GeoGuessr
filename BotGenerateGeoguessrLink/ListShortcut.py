import time

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Lie une URL à un nom (shortcut). Au lieu d'utiliser l'URL vous pouvez utiliser le shortcut.\n"
    msg += "`!!add <url> <shortcut>`\n"
    msg += "`url`: URL de la map.\n"
    msg += "`shortcut`: L'alias utilisable à la place de l'URL."
    return msg

async def handleList(bot, message):
    msg = ""

    for shortcut in bot.shortcuts:
        msg += "Map: `" + bot.shortcuts[shortcut]["title"] + "` -> Alias: `" + shortcut + "`\n"

    return msg