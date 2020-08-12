import time
import Utils
import Generate, Add, ListShortcut, FindShortcut, RandomMap, Help
import os

import discord

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Super secret token to control my bot
TOKEN = os.environ["GEOGUESSR_TOKEN"]

# Command list
commands = []

###################################################################################################
###################################### BOT ########################################################
###################################################################################################

class MyClient(discord.Client):

    # Simple starting
    async def on_ready(self):
        # Options to use to run firefox
        options = Options()
        options.headless = False

        # Firefox
        self.driver = webdriver.Firefox(options=options)

        # If True, the bot is already generating something (and so nothing will happen)
        self.isWorking = False

        # List of shortcuts
        self.shortcuts = {}

        # List of command modules
        self.modules = [Generate, Add, ListShortcut, FindShortcut, RandomMap, Help]

        # List of commands
        self.commands = []
        for module in self.modules:
            self.commands.append(module.command)

        # Help
        self.help = await self.buildHelp()

        # Log in
        await Generate.log(self.driver)

        # Load shortcuts
        await Utils.loadShortcuts(self)

        # print('Logged on as', self.user)
        await client.change_presence(activity=discord.Game(name="!!help"))

    async def buildHelp(self):
        help = discord.Embed(title="Bot GeoGuessr Help")
        help.description = "Toutes les commandes possibles."
        for command in self.commands:
            help.add_field(name=await command.getHelpName(), value=await command.usage(), inline=False)
        return help

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        for command in self.commands:
            if message.content.startswith(command.activation):
                # Split the message
                content = message.content.split(" ")

                # If not enough arguments
                if not await command.isNbArgsCorrect(content):
                    error = "Nombre d'argument invalide!\n"
                    error = error + await command.usage()
                    await message.channel.send(error)
                else:
                    msg, embed = await command.handle(self, command, content)
                    await message.channel.send(msg, embed=embed)
            
###################################################################################################
###################################### MAIN #######################################################
###################################################################################################

if __name__ == "__main__":
    client = MyClient()
    client.run(TOKEN)
