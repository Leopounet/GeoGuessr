import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.commands.Command as Command
from src.commands.CommandReturn import CommandReturn, ErrorType

import src.utils.Utils as Utils

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
    msg += "`shortcut`: The nickname of the URL (shortcut).\n\n"
    msg += "Example: `!!add https://www.geoguessr.com/maps/world World`\n"
    return msg

async def getTitle(bot):
    try:
        return await Utils.getTitle(bot.driver)
    except Exception as _:
        pass
    return None

async def handle(bot, command, message, arguments):

    # get the positional arguments
    url = arguments.get_pos(0)
    name = arguments.get_pos(1)

    # If the url is invalid
    if not await Utils.is_valid_url(url):
        error = "URL is invalid!\n"
        return CommandReturn(error + await usage(), None, ErrorType.UrlError)

    # If the name is already used
    if name in bot.shortcuts:
        error = "This nickname (shortcut) is already used!\n"
        return CommandReturn(error + await usage(), None, ErrorType.ShortcutError)

    # Go to the challenge page
    bot.driver.get(url)
    time.sleep(1)

    # get the title of the challenge
    title = await getTitle(bot)

    # If the url does not lead to a map (has no title)
    if title == None:
        error = "The URL does not lead to a valid Geoguessr map!\n"
        return CommandReturn(error + await usage(), None, ErrorType.NotAMapError)

    # add the shortcut
    bot.shortcuts[name] = {"title": title, "url": url.strip("\n")}

    # message to the user
    msg = "The shortcut " + name + " has been successfully bound the map " + title + "!\n"
    msg += "It now possible to type `!!generate " + name + " [duration]` to generate a map: " + title + " !"

    # save and return
    await Utils.saveShortcuts(bot)
    return CommandReturn(msg)

command = Command.Command()
command.name = "ADD"
command.emojis = [wcm]
command.activation = "!!add"
command.usage = usage
command.handle = handle
command.expected_pos = 2