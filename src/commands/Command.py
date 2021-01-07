import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.utils.Flag as Flag

# Top level command
class Command:

    """
    This stores a command with all the important information in it.
    For more information on how to use it, refer to CommandExample.py.
    """

    def __init__(self):

        """
        Creates a new Command object.
        """

        # Name of the command (diaplayed in help)
        self.name = ""

        # Emojis to use while displaying help (onr or two emojis)
        self.emojis = [""]

        # Activation string (!!generate for example, or !!random)
        self.activation = ""

        # number of expected positional arguments
        self.expected_pos = 0

        # the list of possible flags
        self.flags = Flag.Flag()

        # Handle method
        self.handle = lambda x: "Error"

        # Usage method
        self.usage = lambda x: "Error"

    async def getHelpName(self):
        """
        Returns the name of the command with the set emojis.

        :return: A string representing the name of the command.
        """
        msg = ""
        msg += self.emojis[0]
        msg += " " + self.name + " "
        msg += self.emojis[(len(self.emojis) + 1) % 2]
        return msg