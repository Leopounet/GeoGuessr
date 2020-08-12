import time
import Command
import random
import Generate

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
    msg = "Génère une map aléatoire parmis les shortcuts. " 
    msg += "Si aucune durée n'est précisée, cette dernière est aléatoire aussi.\n"
    msg += "`!!random [duration]`\n"
    msg += "`duration`: La durée d'un round.\n"
    return msg

async def handleRandom(bot, command, content):
    keys = list(bot.shortcuts.keys())

    # Si il n'existe aucun shortcut
    if len(keys) == 0:
        return "Aucun shortcut n'a été sauvegardé!"

    duration = "0"
    if len(content) == 2:
        duration = content[1]
    else:
        duration = str(random.randint(minTime, maxTime))

    msg = "!!generate " + bot.shortcuts[random.choice(keys)]["url"].strip("\n") + " " + duration
    return await Generate.handle(bot, Generate.command, msg.split(" "))

command = Command.Command()
command.name = "RANDOM"
command.emojis = [thinking]
command.activation = "!!random"
command.nbArgs = [1, 2]
command.usage = usage
command.handle = handleRandom