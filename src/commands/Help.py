import os
import sys
import discord
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.commands.Command as Command
from src.commands.CommandReturn import CommandReturn

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use (help)
thumbsup = ":thumbsup:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Prints this help or specific help for another command.\n"
    msg += "`!!help [cmd]`\n"
    msg += "`cmd` (opt): The name of the command to get the help for.\n\n"
    msg += "Example: `!!help`\n"
    msg += "Example: `!!help add`\n"
    return msg

async def get_command(bot, cmd_str):

    # converts a string to a command if possible
    cmd_str = cmd_str.lower()

    # checks all the commands name to see if one corresponds to cmd_str
    for command in bot.commands:
        if command.name.lower() == cmd_str:
            return command
    return None

async def handle(bot, command, message, arguments):

    # get the junk argument if possible (None if there aren't any)
    command = arguments.get_junk(0)

    # if there is a junk argument
    if command != None:

        # get the command corresponding the junk argument (may not be any)
        command = await get_command(bot, command)

        # if there is a corresponding command display its help
        if command != None:
            help = discord.Embed(title=command.name)
            help.add_field(name=await command.getHelpName(), value=await command.usage(), inline=False)
            return CommandReturn("", help)

    # default help
    return CommandReturn("", bot.help)

command = Command.Command()
command.name = "HELP"
command.emojis = [thumbsup]
command.activation = "!!help"
command.usage = usage
command.handle = handle
command.expected_pos = 0