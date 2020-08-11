import time
import Utils, Generate, Add, ListShortcut, FindShortcut

import discord

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Super secret token to control my bot
TOKEN = 'TOKEN'

# Emojis
acc = ":arrows_counterclockwise:"
ac = ":arrows_clockwise:"
tools = ":tools:"
wcm = ":white_check_mark:"
book = ":book:"
question = ":question:"

# Shortcut file
sfile = "shortcuts.txt"

# Shortcut delimiter
sdelimiter = "$$$"

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

        # Help
        self.help = await self.buildHelp()

        # Log in
        await Generate.log(self.driver)

        # Load shortcuts
        await self.loadShortcuts()

        # print('Logged on as', self.user)
        await client.change_presence(activity=discord.Game(name="!!help"))

    async def buildHelp(self):
        help = discord.Embed(title="Bot GeoGuessr Help")
        help.description = "Toutes les commandes possibles."
        help.add_field(name=ac + " GENERATE " + acc, value=await Generate.usage())
        help.add_field(name=tools + " HELP " + tools, value="Génère cette aide.\n`!!help`", inline=False)
        help.add_field(name=wcm + " ADD " + wcm, value=await Add.usage(), inline=False)
        help.add_field(name=book + " LIST " + book, value=await ListShortcut.usage(), inline=False)
        help.add_field(name=question + " FIND URL " + question, value=await FindShortcut.usage(), inline=False)
        return help

    async def loadShortcuts(self):
        try:
            with open(sfile, "r") as f:
                for line in f:
                    line = line.split(sdelimiter)
                    if len(line) == 3:
                        self.shortcuts[line[0]] = {"title": line[1], "url": line[2]}
        except Exception as _:
            pass

    async def saveShortcuts(self):
        with open(sfile, "w") as f:
            for shortcut in self.shortcuts:
                line = shortcut + sdelimiter 
                line += self.shortcuts[shortcut]["title"] + sdelimiter 
                line += self.shortcuts[shortcut]["url"] + "\n"
                f.write(line)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        # generate map
        if message.content.startswith('!!generate'):
            if not self.isWorking:
                self.isWorking = True
                msg = await Generate.handleGenerate(self, message)
                await message.channel.send(msg)
                self.isWorking = False

        # Adds shortcuts
        if message.content.startswith("!!add"):
            msg = await Add.handleAdd(self, message)
            await message.channel.send(msg)
            await self.saveShortcuts()

        # display help
        if message.content.startswith('!!help'):
            await message.channel.send(embed=self.help)

        # display all added shortcuts
        if message.content.startswith("!!list"):
            msg = await ListShortcut.handleList(self, message)
            await message.channel.send(msg)

        # find shortcut
        if message.content.startswith("!!find"):
            msg = await FindShortcut.handleFind(self, message)
            await message.channel.send(msg)
            

###################################################################################################
###################################### MAIN #######################################################
###################################################################################################

if __name__ == "__main__":
    client = MyClient()
    client.run(TOKEN)