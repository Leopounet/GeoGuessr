import time
import Command

from CommandReturn import CommandReturn, ErrorType

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use (help)
scroll = ":scroll:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Prints the last N archives.\n"
    msg += "`!!archive <N>`\n"
    msg += "`N`: Number of archives to print.\n"
    return msg

async def handle(bot, command, message, content):
    msg = ""
    nb = 0

    try:
        nb = int(content[1])
    except:
        error = "Invalid archive number!"
        return CommandReturn(error + await usage(), None, ErrorType.InvalidNumberError)

    if nb < 0:
        error = "N max: " + str(bot.maxArchives)
        return CommandReturn(error + await usage(), None, ErrorType.InvalidNumberError)

    if nb >= bot.maxArchives:
        nb = bot.maxArchives

    for archive in range(bot.archives.current):
        if nb == 0:
            break
        archive = bot.archives.get(bot.archives.current - archive - 1)
        msg += archive["who"] + " requested " + archive["title"]
        msg += ": " + archive["url"] + " " + archive["duration"] + "\n"
        nb -= 1

    if msg == "":
        msg = "No archives!"

    return CommandReturn(msg)

command = Command.Command()
command.name = "ARCHIVE"
command.emojis = [scroll]
command.activation = "!!archive"
command.nbArgs = [2]
command.usage = usage
command.handle = handle