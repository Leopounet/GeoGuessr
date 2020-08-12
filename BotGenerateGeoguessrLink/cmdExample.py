import Command

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
async def usage():
    msg = "Display the given string.\n"
    msg += "`!!example <str>`\n"
    msg += "`str`: The string to display.\n"
    return msg

# What does you command do?
# bot -> The discord bot and all its information (find more in BotGeoguessr.py)
# command -> The current command (that's what's defined below the handle method)
# message -> The raw message received by the bot (it's DISCORD message, not a string)
# content -> The string received and split along its spaces (so it's an array)
async def handle(bot, command, message, content):
    # The number of argument is checked before this method is called so
    # it is okay to be reckless here
    for c in content:
        msg += c

    # The message the bot should display.
    # msg -> The raw string
    # None -> This could be an embed message instead/in addition (see discord's documentation)
    # in BotGeoguessr.py, await message.channel.send(msg, embed=embed) where msg is msg here, and
    # embed is None
    return msg, None

# Create a command object
command = Command.Command()

# Name to display in the help
command.name = "LIST"

# Emojis to use (one or two)
command.emojis = [book]

# What should you type to activate this command?
# Here typing !!example will trigger this command
# So for example: !!example kne klneln will make the bot send back
# !!example kne klneln will
command.activation = "!!example"

# How many args?
# If the list contain only one number, than it has to be exactly this number of args
# otherwise it has to be between the first and second number
command.nbArgs = [2, 400]

# Setting the two methods defining this command (you shouldn't have to change that
# unless you change the name of the above methods)
command.usage = usage
command.handle = handle