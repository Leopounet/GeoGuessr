import time
import Command

import Generate, Utils, RandomMap

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
    msg += "`!!+generate <N> [map_url] [duration]`\n"
    msg += "`N`: Le nombre de maps à générer.\n"
    msg += "`map_url` (opt): Url vers la map à générer (peut aussi être un shortcut). Si non précisé, random.\n"
    msg += "`duration` (opt): Durée d'un round en secondes.\n"
    return msg

async def handle(bot, command, message, content):
    nb = 0
    duration = ""

    try:
        nb = int(content[1])
    except Exception as _:
        error = "N n'est pas une valeur valide!"
        return error + await usage(), None
        
    if len(content) == 4:
        try:
            duration = int(content[3])
        except Exception as _:
            error = "Durée invalide!"
            return error + await usage(), None

    if len(content) == 2:
        for _ in range(nb):
            res, _ = await RandomMap.handle(bot, RandomMap.command, message, ["!!random"])
            await message.channel.send(res)
    else:
        for _ in range(nb):
            res, _ = await Generate.handle(bot, Generate.command, message, ["!!generate", content[2], duration])
            await message.channel.send(res)
    return "Done!", None

command = Command.Command()
command.name = "GENERATE+"
command.emojis = [acc, ac]
command.activation = "!!+generate"
command.nbArgs = [2, 4]
command.usage = usage
command.handle = handle