import os
import sys
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.commands.Command as Command
import src.commands.Generate as Generate
import src.commands.RandomMap as RandomMap
import src.utils.ArgumentReader as ArgumentReader
from src.commands.CommandReturn import CommandReturn, ErrorType

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Emojis (help display)
acc = ":arrows_counterclockwise:"
ac = ":arrows_clockwise:"

map_flag = "-m"
duration_flag = "-d"
no_move_flag = "-n"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Generates N times the requested map.\n"
    msg += "`!!+generate <N> [-m map_url] [-d duration] [-n]`\n"
    msg += "`N`: The number of maps to generate.\n"
    msg += "`-m [map_url]` (opt): URL to the map to generate (or a nickname/shortcut)."
    msg += " If none is specified this will be random.\n"
    msg += "`-d [duration]` (opt): Duration of a round min:sec (unlimited by default).\n"
    msg += "`-n` (opt): If set, no movement will be allowed.\n\n"
    msg += "Example: `!!generate+ 5`\n"
    msg += "Example: `!!generate+ 10 -m https://www.geoguessr.com/maps/world`\n"
    msg += "Example: `!!generate+ -d 1:20 -m https://www.geoguessr.com/maps/world 10`\n"
    msg += "Example: `!!generate+ 5 -d 3:00 -n`\n"
    return msg

async def handle(bot, command, message, arguments):

    # the number of map to generate
    nb = 0

    # the duration of a round
    duration = "0"

    # try block in case the strign is not a number
    try:
        nb = int(arguments.get_pos(0))

    # if the string is not a number, abort
    except Exception as _:
        error = "Invalid number of maps to generate!\n"
        return CommandReturn(error + await usage(), None, ErrorType.InvalidNumberError)

    next_map = ""
    # generate the requested number of maps
    for _ in range(nb):

        # get the next map to generate
        if not arguments.is_flag_set(map_flag):
            next_map = random.choice(list(bot.shortcuts.keys()))
        else:
            next_map = arguments.get_non_pos(map_flag)[0]

        # artificially create the list of argument to call Generate
        gen_args = ArgumentReader.ArgumentList()
        gen_args.add_pos(next_map)

        if arguments.is_flag_set(duration_flag):
            gen_args.add_non_pos(duration_flag, arguments.get_non_pos(duration_flag))

        if arguments.is_flag_set(no_move_flag):
            gen_args.add_non_pos(no_move_flag, arguments.get_non_pos(no_move_flag))

        # call Generate command
        res = await Generate.handle(bot, Generate.command, message, gen_args)
        await message.channel.send(res.msg)
    return CommandReturn("Done!")

command = Command.Command()
command.name = "GENERATE+"
command.emojis = [acc, ac]
command.activation = "!!generate+"
command.usage = usage
command.handle = handle

command.expected_pos = 1

# map flag
command.flags.add_flag(map_flag, 1)

# duration flag
command.flags.add_flag(duration_flag, 1)

# no-move flag
command.flags.add_flag(no_move_flag, 0)