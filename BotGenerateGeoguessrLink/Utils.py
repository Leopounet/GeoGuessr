import subprocess, time, random

from selenium.webdriver.common.by import By

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# When doing a curl request, check that many characters for the response's code
lookup200 = 15

# Not a number error
NAN = None

# Path to the title of the map
xpath_title = "/html/body/div/div/main/div/div/div[1]/div[1]/div[2]/h1"

# Shortcut file
sfile = "shortcuts.txt"

# Shortcut delimiter
sdelimiter = "$$$"

# List of chars
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789="

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

# Executes a command with bash
def execute(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    return process.communicate()

# How to use the bot
async def usage():
    msg = "!!generate <map_url> [duration]\nSi duration n'est pas précisé, temps infini."
    return msg

# Casts a string to an int
# Returns NAN if not a number
async def strToInt(value):
    try:
        return int(value)
    except Exception as _:
        return NAN
    return NAN

async def timeToInt(value):
    try:
        if ":" in value:
            value = value.split(":")
            minutes = value[0]
            seconds = value[1]
            return int(minutes) * 60 + int(seconds)
        return int(value)
    except Exception as _:
        return NAN
    return NAN

# Checks if a given URL is valid
async def isValidURL(url):
    output, _ = execute("curl --head -s " + url)
    output = output.decode("utf-8")

    # Look at the head of the response after curl, if the first few characters do not
    # contain 200, the URL can't be used
    if "200" in output[:lookup200]:
        return True
    return False

# Get the title of the map
async def getTitle(driver):
    return driver.find_element(By.XPATH, xpath_title).text

# Loads all shortcuts
async def loadShortcuts(bot):
        try:
            with open(sfile, "r") as f:
                for line in f:
                    line = line.split(sdelimiter)
                    if len(line) == 3:
                        bot.shortcuts[line[0]] = {"title": line[1], "url": line[2]}
        except Exception as _:
            pass

async def saveShortcuts(bot):
    with open(sfile, "w") as f:
        for shortcut in bot.shortcuts:
            line = shortcut + sdelimiter 
            line += bot.shortcuts[shortcut]["title"] + sdelimiter 
            line += bot.shortcuts[shortcut]["url"] + "\n"
            f.write(line)

async def generateRandomString(length):
    res = ""
    for _ in range(length):
        res += random.choice(res)
    return res

class MyQueue:

    def __init__(self, size):

        # The list
        self.queue = []

        # The max size
        self.size = size

        # Current nb of elements
        self.current = 0

    def add(self, value):
        if self.current < self.size:
            self.queue.append(value)
            self.current += 1
        else:
            self.queue = self.queue[1:]
            self.queue.append(value)

    def get(self, index):
        if 0 <= index < self.current:
            return self.queue[index]
        return None
