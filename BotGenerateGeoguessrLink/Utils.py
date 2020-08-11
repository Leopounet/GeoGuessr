import subprocess, time

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