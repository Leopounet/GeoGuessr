import time
import Command
import random
import Generate

from CommandReturn import CommandReturn, ErrorType

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use
thinking = ":thinking:"

# min and max time
minTime = 0
maxTime = 600

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Generates a random map among the given shortcuts." 
    msg += "If no duration is specified, this will be random as well.\n"
    msg += "`!!random [duration]`\n"
    msg += "`duration`: Duration of a round.\n"
    return msg

async def handle(bot, command, message, content):
    keys = list(bot.shortcuts.keys())

    # Si il n'existe aucun shortcut
    if len(keys) == 0:
        msg = "No shortcut has been saved!"
        return CommandReturn(msg)

    duration = "0"
    if len(content) == 2:
        duration = content[1]
    else:
        duration = str(random.randint(minTime, maxTime))

    msg = "!!generate " + bot.shortcuts[random.choice(keys)]["url"].strip("\n") + " " + duration
    return await Generate.handle(bot, Generate.command, message, msg.split(" "))

command = Command.Command()
command.name = "RANDOM"
command.emojis = [thinking]
command.activation = "!!random"
command.nbArgs = [1, 2]
command.usage = usage
command.handle = handle