import time
import Command

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use (help)
scroll = ":scroll:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Affiche les N dernières archives.\n"
    msg += "`!!archive <N>`\n"
    msg += "`N`: Le nombre d'archives à afficher.\n"
    return msg

async def handle(bot, command, message, content):
    msg = ""
    nb = 0

    try:
        nb = int(content[1])
    except:
        error = "Nombre d'archives invalide!"
        return error + await usage(), None

    if nb < 0:
        error = "N max: " + str(bot.maxArchives)
        return error + await usage(), None

    if nb >= bot.maxArchives:
        nb = bot.maxArchives

    for archive in bot.archives:
        if nb == 0:
            break
        msg += bot.archives[archive]["who"] + " requested " + bot.archives[archive]["title"]
        msg += ": " + archive + " " + bot.archives[archive]["duration"] + "\n"
        nb -= 1

    if msg == "":
        msg = "Aucune archive!"

    return msg, None

command = Command.Command()
command.name = "ARCHIVE"
command.emojis = [scroll]
command.activation = "!!archive"
command.nbArgs = [2]
command.usage = usage
command.handle = handle