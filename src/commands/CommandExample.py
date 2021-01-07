import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.commands.Command as Command
from src.commands.CommandReturn import CommandReturn, ErrorType

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# This is the emoji to display when showing help (you can either set one or two of those
# in which case the first one will be displayed on the left of the name of the command
# and the second one on the right)
book = ":book:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

# What is the generic error message?
# a command is designed the following way:
# 
# it has an activation string, here its "!!example"
# 
# it has a list of mandatory arguments (positional arguments)
# here "str" is a mandatory argument
# 
# and it has a list of not mandatory arguments (non positional arguments)
# here -n [times] is a non positional argument that requires an additional value
async def usage():
    msg = "Display the given string a certain amount of time.\n"
    msg += "`!!example <str> [-n times]`\n"
    msg += "`str`: The string to display.\n"
    msg += "`-n [times]` (opt): The number of times the string should be displayed (default: 1).\n\n"
    msg += "Example: `!!example Hello`\n"
    msg += "Example: `!!example Hello -n 3`\n"
    msg += "Example: `!!example -n 3 Hi`\n"
    return msg

# What does you command do?
# bot -> The discord bot and all its information (find more in BotGeoguessr.py)
# command -> The current command (that's what's defined below the handle method)
# message -> The raw message received by the bot (it's DISCORD message, not a string)
# arguments -> An ArgumentList object that contains all the positional, non positional
#              and junk arguments (the latter refers to arguments that should not be here)
#              Check the file ArgumentReader for more info though
async def handle(bot, command, message, arguments):

    # this string will be the final message returned
    msg = ""

    # first let's get the string that we want to print by getting the first positional
    # argument
    # note that this can NOT fail unless the value you use is bigger than the 
    # expected number of positional arguments because the number of positional
    # is checked before hand in BotGeoguessr.py
    string_to_print = arguments.get_pos(0)

    # this will store how many times we want to print the string
    n = 1

    # then let's check if the non positional argument -n is set
    if arguments.is_flag_set("-n"):

        # if it is set, then we get its value
        val = arguments.get_non_pos("-n")

        # this value is a list (because there could be multiple
        # expected value for this non positional argument)
        # we know there is only one argument here so we can directly get it
        val = val[0]

        # this argument is now a string and hopefully it is a number
        # let's convert it to an int
        # to do that we need a try block, in case the string is not a number
        try:
            val = int(val)
        
        # if the given number is invalid, let's abort the whole command
        # (it's not something you want to do for non positional arguments
        # most of the time as they are optional, so them being invalid should 
        # not break anything but here it shows how to return an error)
        except Exception as _:
            return CommandReturn("Invalid number!", error=ErrorType.InvalidNumberError)

        # finally, if the value is positive, and not too big, we can set n to it
        if 0 < val <= 100:
            n = val

    # let's construct the final message to send
    for i in range(n):
        msg += string_to_print + "\n"

    # finally we can return the message the bot will send
    return CommandReturn(msg)


# Create a command object
command = Command.Command()

# Name to display in the help
command.name = "EXAMPLE"

# Emojis to use (one or two)
command.emojis = [book]

# What should you type to activate this command?
# Here typing !!example will trigger this command
command.activation = "!!example"

# Set the number of expected positional arguments
command.expected_pos = 1

# Set the non positional flags you want to use
# the first argument is the flag
# the second is the number of values that should follow your flag
command.flags.add_flag("-n", 1)

# Setting the two methods defining this command (you shouldn't have to change that
# unless you change the name of the above methods)
command.usage = usage
command.handle = handle
