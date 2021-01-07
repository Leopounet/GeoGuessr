import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.commands.Command as Command
from src.commands.CommandReturn import CommandReturn, ErrorType

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
    msg += "`N`: Number of archives to print.\n\n"
    msg += "Example: `!!archive 10`"
    return msg

async def handle(bot, command, message, arguments):

    # the message to return
    msg = ""

    # the number of archives to get
    nb = 0

    # try (in case the string is not a number)
    try:

        # get the first positional argument
        nb = int(arguments.get_pos(0))

    # if the first positional argument is not a number, stop here
    except:
        error = "Invalid archive number!"
        return CommandReturn(error + await usage(), None, ErrorType.InvalidNumberError)

    # if the number of archives wanted is not positive, stop here
    if nb <= 0:
        error = "N max: " + str(bot.maxArchives)
        return CommandReturn(error + await usage(), None, ErrorType.InvalidNumberError)

    # if the number of archives is too big, make it the maximum possible
    if nb >= bot.maxArchives:
        nb = bot.maxArchives

    # create a message with all the archives
    for archive in range(bot.archives.current):

        # if the requested number of archives has been reached
        if nb == 0:
            break

        # add the archives to the message wit ha bit extra data
        archive = bot.archives.get(bot.archives.current - archive - 1)
        msg += archive["who"] + " requested " + archive["title"]
        msg += ": " + archive["url"] + " " + archive["duration"] + "\n"

        # counter reduction
        nb -= 1

    # if the message is empty that means that there are no archives
    if msg == "":
        msg = "No archives!"

    return CommandReturn(msg)

command = Command.Command()
command.name = "ARCHIVE"
command.emojis = [scroll]
command.activation = "!!archive"
command.usage = usage
command.handle = handle
command.expected_pos = 1