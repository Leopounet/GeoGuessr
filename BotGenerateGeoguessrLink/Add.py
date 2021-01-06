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
    msg = "Binds a URL to a nickname (shortcut). Instead of using the URL, allows to type `!!generate <shortcut>`.\n"
    msg += "`!!add <url> <shortcut>`\n"
    msg += "`url`: URL of the map.\n"
    msg += "`shortcut`: The nickname of the URL (shortcut)."
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
        error = "URL is invalid!\n"
        return CommandReturn(error + await usage(), None, ErrorType.UrlError)

    if name in bot.shortcuts:
        error = "This nickname (shortcut) is already used!\n"
        return CommandReturn(error + await usage(), None, ErrorType.ShortcutError)

    # Go to the challenge page
    bot.driver.get(url)
    time.sleep(1)

    title = await getTitle(bot)

    # If the url is not a map
    if title == None:
        error = "The URL does not lead to a valid Geoguessr map!\n"
        return CommandReturn(error + await usage(), None, ErrorType.NotAMapError)

    bot.shortcuts[name] = {"title": title, "url": url.strip("\n")}

    msg = "The shortcut " + name + " has been successfully bound the map " + title + "!\n"
    msg += "It now possible to type `!!generate " + name + " [duration]` to generate a map: " + title + " !"

    await Utils.saveShortcuts(bot)

    return CommandReturn(msg)

command = Command.Command()
command.name = "ADD"
command.emojis = [wcm]
command.activation = "!!add"
command.nbArgs = [3]
command.usage = usage
command.handle = handle