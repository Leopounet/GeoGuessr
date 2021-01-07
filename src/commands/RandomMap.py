import os
import sys
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.commands.Command as Command
import src.commands.Generate as Generate
import src.utils.ArgumentReader as ArgumentReader
import src.utils.Utils as Utils
from src.commands.CommandReturn import CommandReturn

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emoji to use
thinking = ":thinking:"

# min and max time
minTime = 0
maxTime = 600

# possible flags
duration_flag = "-d"
random_duration_flag = "-rd"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Generates a random map among the given shortcuts." 
    msg += "If no duration is specified, time is unlimited.\n"
    msg += "`!!random [-d duration] [-rd min-duration max-duration]`\n"
    msg += "`-d [duration]` (opt): Duration of a round (incompatible with -rd).\n"
    msg += "`-rd [min] [max]` (opt): Allows to generate random durations for a round, the duration"
    msg += " will be between min and max (if max < min, time is unlimited).\n\n"
    msg += "Example: `!!random`\n"
    msg += "Example: `!!random -d 1:20`\n"
    msg += "Example: `!!random -rd 1:20 5:00`"
    return msg

async def handle(bot, command, message, arguments):

    # all the possible shortcuts
    keys = list(bot.shortcuts.keys())

    #  If no shortcut exists
    if len(keys) == 0:
        msg = "No shortcut has been saved!"
        return CommandReturn(msg)

    # create a new arg list for generate
    gen_args = ArgumentReader.ArgumentList()

    # generate a random map
    gen_args.add_pos(random.choice(keys))

    # set teh duration
    if arguments.is_flag_set(duration_flag):
        gen_args.add_non_pos(duration_flag, arguments.get_non_pos(duration_flag))

    # set the random duration
    if arguments.is_flag_set(random_duration_flag):
        min_duration = await Utils.time_to_int(arguments.get_non_pos(random_duration_flag)[0])
        max_duration = await Utils.time_to_int(arguments.get_non_pos(random_duration_flag)[1])

        if(min_duration != Utils.NAN and max_duration != Utils.NAN and 0 < min_duration <= max_duration):
            gen_args.add_non_pos(duration_flag, [str(random.randint(min_duration, max_duration))])

    return await Generate.handle(bot, Generate.command, message, gen_args)

command = Command.Command()
command.name = "RANDOM"
command.emojis = [thinking]
command.activation = "!!random"
command.usage = usage
command.handle = handle

command.expected_pos = 0

# duration flag
command.flags.add_flag(duration_flag, 1)

# random duration flag flag
command.flags.add_flag(random_duration_flag, 2)