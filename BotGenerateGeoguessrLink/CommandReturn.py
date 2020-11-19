from enum import Enum

class ErrorType(Enum):
    DurationError = 0
    UrlError = 1
    UnknownError = 2
    ShortcutError = 3
    NotAMapError = 4
    InvalidNumberError = 5
    BusyBotError = 6


class CommandReturn:

    def __init__(self, msg="", embed=None, error=None):
        
        self.msg = msg

        self.embed = embed

        self.error = error