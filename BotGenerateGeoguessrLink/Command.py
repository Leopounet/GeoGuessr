# Top level command
class Command:

    def __init__(self):

        # Name of the command (diaplayed in help)
        self.name = ""

        # Emojis to use while displaying help (onr or two emojis)
        self.emojis = [""]

        # Activation string (!!generate for example, or !!random)
        self.activation = ""

        # Number of expecte arguments (range)
        self.nbArgs = [0, 0]

        # Handle method
        self.handle = lambda x: "Error"

        # Usage method
        self.usage = lambda x: "Error"

    async def getHelpName(self):
        msg = ""
        msg += self.emojis[0]
        msg += " " + self.name + " "
        msg += self.emojis[(len(self.emojis) + 1) % 2]
        return msg

    async def isNbArgsCorrect(self, content):
        if len(self.nbArgs) == 1:
            return self.nbArgs[0] == len(content)
        return len(content) >= self.nbArgs[0] and len(content) <= self.nbArgs[1]