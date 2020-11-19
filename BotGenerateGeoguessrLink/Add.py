import time

import Utils
import Command
from CommandReturn import CommandReturn, ErrorType

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

wcm = ":white_check_mark:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Lie une URL à un nom (shortcut). Au lieu d'utiliser l'URL vous pouvez utiliser le shortcut.\n"
    msg += "`!!add <url> <shortcut>`\n"
    msg += "`url`: URL de la map.\n"
    msg += "`shortcut`: L'alias utilisable à la place de l'URL."
    return msg

async def getTitle(bot):
    try:
        return await Utils.getTitle(bot.driver)
    except Exception as _:
        return None
    return None

async def handle(bot, command, message, content):
    # url : name
    url = content[1]
    name = content[2]

    # If the name is already used or the url is invalid
    if not await Utils.isValidURL(url):
        error = "L'URL n'est pas valide!\n"
        return CommandReturn(error + await usage(), None, ErrorType.UrlError)

    if name in bot.shortcuts:
        error = "Le shortcut est déjà utilisé!\n"
        return CommandReturn(error + await usage(), None, ErrorType.ShortcutError)

    # Go to the challenge page
    bot.driver.get(url)
    time.sleep(1)

    title = await getTitle(bot)

    # If the url is not a map
    if title == None:
        error = "L'URL ne pointe pas vers une map GeoGuessr!\n"
        return CommandReturn(error + await usage(), None, ErrorType.NotAMapError)

    bot.shortcuts[name] = {"title": title, "url": url.strip("\n")}

    msg = "Le raccourci " + name + " vers la map " + title + " a été ajouté!\n"
    msg += "Il est à présent possible de taper `!!generate " + name + " [duration]` pour générer une map " + title + " !"

    await Utils.saveShortcuts(bot)

    return CommandReturn(msg)

command = Command.Command()
command.name = "ADD"
command.emojis = [wcm]
command.activation = "!!add"
command.nbArgs = [3]
command.usage = usage
command.handle = handle