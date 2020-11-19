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
    msg = "Génère N fois la map demandée.\n"
    msg += "`!!+generate <N> [map_url] [duration] [no-move`\n"
    msg += "`N`: Le nombre de maps à générer.\n"
    msg += "`map_url` (opt): Url vers la map à générer (peut aussi être un shortcut). Si non précisé, random.\n"
    msg += "`duration` (opt): Durée d'un round en secondes ou au format min:sec.\n"
    msg += "`no-move` (opt): True (ou un alias valide) pour jouer en no move.\n"
    return msg

async def handle(bot, command, message, content):
    nb = 0
    duration = "0"

    try:
        nb = int(content[1])
    except Exception as _:
        error = "N n'est pas une valeur valide!"
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