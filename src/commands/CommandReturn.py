import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from enum import Enum

class ErrorType(Enum):

    """
    Enum of all the possible errors (so far).
    """

    DurationError = 0
    UrlError = 1
    UnknownError = 2
    ShortcutError = 3
    NotAMapError = 4
    InvalidNumberError = 5
    BusyBotError = 6


class CommandReturn:

    """
    Structure to store some information about the return value of a command.
    """

    def __init__(self, msg="", embed=None, error=None):

        """
        Creates a new CommandReturn object.

        :param msg: The message that the bot will send on Discord.

        :param embed: The message to return but embed (if this is set, then msg
        should not be set).

        :param error: The error that occurred, if any.
        """
        
        self.msg = msg

        self.embed = embed

        self.error = error