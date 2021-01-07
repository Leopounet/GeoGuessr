import subprocess
import os
import sys
import discord
import time
import importlib.util
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# list of not commands file (update if needed!)
not_command_files = ["Command.py", "CommandReturn.py", "__init__.py"]

# Page to log in GeoGuessr
loginPage = "https://www.geoguessr.com/signin"

# My mail
mail = os.environ["MAIL"]

# My password
password = os.environ["PASSWD"]

# XPATH for log method
xpath_createAccount = "/html/body/div/section/div/div[2]/button[2]"
xpath_signIn = "/html/body/div[1]/div/div/header/div[2]/div/div[1]/a"
xpath_google = "/html/body/div[1]/div/main/div/div/div/div/div/section/div/div[2]/button"
xpath_mail = "//*[@id=\"identifierId\"]"
xpath_mailNext = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]"
xpath_password = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
xpath_passwordNext = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

def execute(command):
    """
    Executes a bash command.

    :param command: The bash command to execute.
    """
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    return process.communicate()

async def time_to_int(value):
    """
    Converts a string representing a time value to an int.

    :param value: The string to convert, can either be a string \
    representing a normal int or a string of the format min:sec.

    :return: The correspoding integer if possible, NAN otherwise.
    """

    # try block in case the string is incorrect
    try:

        # if it is the format min:sec
        if ":" in value:
            value = value.split(":")
            minutes = value[0]
            seconds = value[1]
            return int(minutes) * 60 + int(seconds)

        # otherwise convert directly
        return int(value)

    # in case of an error return NAN (pass just to have the return all the way down)
    except Exception as _:
        pass
    return NAN

async def int_to_time(value):
    """
    Converts an int to a corresponding time.

    :param value: The int to convert.

    :return: The corresponding string.
    """
    minutes = value // 60
    seconds = value % 60

    if seconds == 0:
        seconds = "00"
        
    return str(minutes) + ":" + str(seconds)

# Checks if a given URL is valid
async def is_valid_url(url):
    """
    Checks if the given URL is a valid URL.

    :param url: The URL to test.

    :return: True if the URL is valid, False otherwise.
    """

    try:
        # curl to check if the URL is valid by getting the code
        output, _ = execute("curl --head -s " + url)
        output = output.decode("utf-8")

        # Look at the head of the response after curl, if the first few characters do not
        # contain 200, the URL can't be used
        if "200" in output[:lookup200]:
            return True
        return False
    except Exception as _:
        pass
    return False

async def get_title(driver):
    """
    Get the title of the Geoguessr map.

    :param driver: The browser to use.

    :return: A string corresponding to the title of the map.
    """
    return driver.find_element(By.XPATH, xpath_title).text

async def load_shortcuts(bot):
    """
    Loads all the shortcuts from the shortcuts.txt file.

    :param bot: The bot to load the shortcuts in.
    """

    # try block in case the file does not exist
    try:

        # open the shortcut file
        with open(sfile, "r") as f:

            # read all the lines
            for line in f:

                # use the delimiter to have all information split
                line = line.split(sdelimiter)

                # add the shortcut to the list of shortcut
                if len(line) == 3:
                    bot.shortcuts[line[0]] = {"title": line[1], "url": line[2]}

    # in case of an error, do nothing
    except Exception as _:
        pass

async def save_shortcuts(bot):
    """
    Saves the current list of shortcuts stored in the bot.

    :param bot: The bot to read the shortcuts from.
    """

    # open the saving file
    with open(sfile, "w") as f:

        # for every shortcut
        for shortcut in bot.shortcuts:

            # write them down in this specific format
            line = shortcut + sdelimiter 
            line += bot.shortcuts[shortcut]["title"] + sdelimiter 
            line += bot.shortcuts[shortcut]["url"] + "\n"
            f.write(line)

async def get_all_command_modules():
    """
    Returns the list of modules corresponding to a Command.

    :return: A list of modules.
    """

    # the path to the list of commands
    command_path = "commands/"

    # all the command file in the commands directory
    onlyfiles = [f for f in os.listdir(command_path) if os.path.isfile(os.path.join(command_path, f))]

    # the final list of modules
    res = []

    # for every file in the commands directory
    for f in onlyfiles:

        # if it is a special non command file specified above, skip
        if f in not_command_files:
            continue
        
        # load the module
        path = command_path + f
        name = f[:-3]
        spec = importlib.util.spec_from_file_location(name, path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        res.append(foo)

    return res

async def build_help(commands):

    """
    Creates a string correspoding to the default help returned by the bot.

    :param commands: The list commands defined for the bot.

    :return: A string corresponding to the default help of the bot.
    """

    # this code is """"slow"""" as in it could be better but given there will never be
    # a lot of commands, this is fine

    # create a new embed
    help = discord.Embed(title="Bot GeoGuessr Help")

    # the list of commands name
    all_cmd = []

    # get all the commands name
    for command in commands:
        all_cmd.append(command.name)
    
    # sort the names
    all_cmd = sorted(all_cmd)

    # the final string
    res = ""

    # create the final string by appending the command names
    for cmd in all_cmd:
        res += cmd + "\n"

    # final touch
    res = res + "\n"
    res += "For more information use `!!help [cmd]`\n"
    res += "Example: `!!help add`"

    help.add_field(name="All possibles commands.", value=res)
    return help

def get_element(driver, xpath, max_timeout=5):
    """
    Gets an element from the browser given its XPATH.

    :param driver: The webbrowser to use.

    :param xpath: The XPATH of the element to get.

    :param max_timeout: The maximum amount of time to wait before aborting.

    :return: An element of the page.
    """
    element = WebDriverWait(driver, max_timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    time.sleep(0.8)
    return element

async def log(driver):

    """
    Logs the user in Geoguessr.

    :param driver: The webbrowser to log in.
    """

    # Get to the log in page
    driver.get(loginPage)

    time.sleep(1)

    # Log in with google
    get_element(driver, xpath_google).click()
    
    # If everything is working fine, a new window has been opened
    if len(driver.window_handles) > 1:

        # Log in
        driver.switch_to.window(driver.window_handles[1])
        get_element(driver, xpath_mail).send_keys(mail)
        get_element(driver, xpath_mailNext).click()

        get_element(driver, xpath_password).send_keys(password)
        get_element(driver, xpath_passwordNext).click()
        driver.switch_to.window(driver.window_handles[0])

    time.sleep(5)

async def is_logged(driver):

    """
    Checks if the user is logged in Geoguessr.

    :param driver: The web browser to check in.

    :return: True if the user is logged in, False otherwise.
    """

    # Look for the "Create Account" button
    try:
        driver.find_element(By.XPATH, xpath_createAccount)
    except Exception as _:

        # Look for the "Sign In" button
        try:
            driver.find_element(By.XPATH, xpath_signIn)
        except Exception as _:
            return True
    return False