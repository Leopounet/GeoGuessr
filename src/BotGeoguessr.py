import os
import sys
import discord
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import src.utils.Utils as Utils
import src.utils.Queue as Queue
from src.utils.ArgumentReader import ArgumentReader

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Super secret token to control my bot
TOKEN = os.environ["GEOGUESSR_TOKEN"]

# options for selenium
options = Options()
options.headless = True

###################################################################################################
###################################### BOT ########################################################
###################################################################################################

class BotGeoguessr(discord.Client):

    """
    This is the main class, this represents the Bot that will yield
    geoguessr maps.
    """

    # Simple starting
    async def on_ready(self):

        """
        This method is called when the bot starts.
        """

        # List of all command file
        self.modules = await Utils.get_all_command_modules()

        # Firefox
        self.driver = webdriver.Firefox(options=options)

        # If True, the bot is already generating something (and so nothing will happen)
        self.is_working = False

        # List of shortcuts
        self.shortcuts = {}

        # List of commands
        self.commands = []
        for module in self.modules:
            self.commands.append(module.command)

        # Help
        self.help = await Utils.build_help(self.commands)

        # Max archives
        self.maxArchives = 20

        # Archives
        self.archives = Queue.Queue(self.maxArchives)

        # Log in
        await Utils.log(self.driver)

        # Load shortcuts
        await Utils.load_shortcuts(self)

        # print('Logged on as', self.user)
        await client.change_presence(activity=discord.Game(name="!!help"))

    async def on_message(self, message):
        """
        Handles every received message.

        :param message: The latest message received.
        """

        # Try block, if an error occurs, the bot doesn't crash this way
        try:
            await self.handle_command(message)
        except Exception as e:
            print(e)
            self.is_working = False

    async def handle_command(self, message):
        """
        Handles every command possible.

        :param message: The message that may contain a command.
        """
        
        # don't respond to ourselves
        if message.author == self.user:
            return

        # Split the message
        content = message.content.split(" ")

        # checks if the message contains a valid command
        for command in self.commands:
            
            # if this is the corresponding command
            if content[0] == command.activation:
                
                # get the list of arguments
                arguments = ArgumentReader.read(content[1:], command.flags, command.expected_pos)

                # If not enough arguments
                if arguments.get_nb_pos() != command.expected_pos:
                    error = "Invalid number of arguments!\n"
                    error = error + await command.usage()
                    await message.channel.send(error)

                # if there are enough positional arguments
                else:
                    res = await command.handle(self, command, message, arguments)
                    await message.channel.send(res.msg, embed=res.embed)

###################################################################################################
###################################### MAIN #######################################################
###################################################################################################

if __name__ == "__main__":
    client = BotGeoguessr()
    client.run(TOKEN)
