import time
import Command

import Generate, Utils, RandomMap

from CommandReturn import CommandReturn, ErrorType

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emojis (help display)
acc = ":arrows_counterclockwise:"
ac = ":arrows_clockwise:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Generates N times the requested map.\n"
    msg += "`!!+generate <N> [map_url] [duration] [no-move`\n"
    msg += "`N`: The number of maps to generate.\n"
    msg += "`map_url` (opt): URL to the map to generate (or a nickname/shortcut). If none is specified this will be random.\n"
    msg += "`duration` (opt): Duration of a round min:sec.\n"
    msg += "`no-move` (opt): Set it to True (or any valid alias) to disable movement.\n"
    return msg

async def handle(bot, command, message, content):
    nb = 0
    duration = "0"

    try:
        nb = int(content[1])
    except Exception as _:
        error = "Invalid number of maps to generate!"
        return CommandReturn(error + await usage(), None, ErrorType.InvalidNumberError)

    if len(content) == 2:
        for _ in range(nb):
            res = await RandomMap.handle(bot, RandomMap.command, message, ["!!random"])
            if res.error != None:
                return res
            await message.channel.send(res.msg)
    else:
        if len(content) >= 4:
            duration = content[3]
        no_move = False
        if len(content) >= 5:
            no_move = content[4]
        for _ in range(nb):
            res = await Generate.handle(bot, Generate.command, message, ["!!generate", content[2], duration, no_move])
            if res.error != None:
                return res
            await message.channel.send(res.msg)
    return CommandReturn("Done!")

command = Command.Command()
command.name = "GENERATE+"
command.emojis = [acc, ac]
command.activation = "!!+generate"
command.nbArgs = [2, 5]
command.usage = usage
command.handle = handle