import time, os

import Utils
import Command

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# Page to log in GeoGuessr
loginPage = "https://www.geoguessr.com/signin"

# My mail
mail = os.environ["MAIL"]

# My password (ugh)
password = os.environ["PASSWD"]

# XPATH LIST
xpath_play = "/html/body/div/div/main/div/div/div[1]/div[3]/button"
xpath_createAccount = "/html/body/div/section/div/div[2]/button[2]"
xpath_signIn = "/html/body/div[1]/div/div/header/div[2]/div/div[1]/a"
xpath_google = "/html/body/div[1]/div/main/div/div/div/div/div/section/div/div[2]/button"
xpath_mail = "//*[@id=\"identifierId\"]"
xpath_mailNext = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]"
xpath_password = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
xpath_passwordNext = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]"
xpath_challenge = "/html/body/div/div/main/div/div/div/div/div/article/div[1]/div/div[2]/label/div[1]"
xpath_time = "/html/body/div/div/main/div/div/div/div/div/article/div[2]/div/div[1]/div[2]"
xpath_inviteFriends = "/html/body/div/div/main/div/div/div/div/div/article/div[2]/button"
xpath_URL = "/html/body/div/div/main/div/div/div/div/div/article/div/div[2]/span/input"

# The time slider factor : 8 to the right = 10 seconds
shift = 8

# Emojis (help display)
acc = ":arrows_counterclockwise:"
ac = ":arrows_clockwise:"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Génère un challenge pour une map spécifiée.\n"
    msg += "`!!generate <map_url> [duration]`\n"
    msg += "`map_url`: Url vers la map à générer (peut aussi être un shortcut).\n"
    msg += "`duration` (opt): Durée d'un round en secondes.\n"
    return msg

# True if the bot is already logged in GeoGuessr
async def isLogged(driver):

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

# Log in GeoGuessr
async def log(driver):

    # Get to the log in page
    driver.get(loginPage)
    time.sleep(1)

    # Log in with google
    driver.find_element(By.XPATH, xpath_google).click()
    time.sleep(2)
    
    # If everything is working fine, a new window has been opened
    if len(driver.window_handles) > 1:

        # Log in
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element(By.XPATH, xpath_mail).send_keys(mail)
        driver.find_element(By.XPATH, xpath_mailNext).click()

        time.sleep(1)
        driver.find_element(By.XPATH, xpath_password).send_keys(password)
        driver.find_element(By.XPATH, xpath_passwordNext).click()
        driver.switch_to.window(driver.window_handles[0])

        # Required wait (going too fast breaks selenium)
        time.sleep(10)

async def setupChallenge(driver, duration):
    # Click on the play button
    driver.find_element(By.XPATH, xpath_play).click()
    time.sleep(0.5)

    # Click on the challenge button
    driver.find_element(By.XPATH, xpath_challenge).click()
    time.sleep(0.5)

    # Slide to the correct duration
    slider = driver.find_element(By.XPATH, xpath_time)
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(int(duration / 10) * shift, 0).release().perform()
    time.sleep(2)

    # Get to the URL of the challenge
    driver.find_element(By.XPATH, xpath_inviteFriends).click()
    time.sleep(0.5)

async def roundDuration(duration):
    # Max is 600, min is 0
    if duration > 600 or duration <= 0:
        return 0

    return int(duration / 10) * 10

async def getTitle(driver):
    try:
        return await Utils.getTitle(driver)
    except Exception as _:
        return None
    return None

# Generates a URL to a challenge with a set duration
async def generateMap(bot, message, driver, url, duration):

    # If the URL is not valid
    if not await Utils.isValidURL(url):
        error = "L'URL n'est pas valide!\n"
        return error + await usage(), None

    # Go to the URL
    driver.get(url)
    time.sleep(1)

    # If the bot is not logged in
    if not await isLogged(driver):
        await log(driver)
        driver.get(url)
        time.sleep(1)

    # Get the name of the map to generate
    title = await getTitle(driver)
    if title == None:
        error = "L'URL ne pointe pas vers une map GeoGuessr!\n"
        return error + await usage(), None

    # Round the duration to a valid number of seconds
    duration = await roundDuration(duration)

    # Setup the challenge
    await setupChallenge(driver, duration)

    msg = title
    challenge = "<" + driver.find_element(By.XPATH, xpath_URL).get_attribute('value') + ">"
    msg += ": " + challenge

    if duration == 0:
        duration = "temps illimité!"
        msg += " " + duration
    else:
        msg += " " + str(duration) + " secondes par rounds!"

    bot.archives.add({"title": title, "who": str(message.author), "duration":str(duration), "url":challenge})

    bot.isWorking = False
    return msg, None

async def handle(bot, command, message, content):
    if bot.isWorking == False:
        bot.isWorking = True

        # Get the URL
        url = content[1]
        if url in bot.shortcuts:
            url = bot.shortcuts[url]["url"]

        duration = 0

        # Get the duration (if specified)
        if len(content) == 3:
            duration = await Utils.strToInt(content[2])
            if duration == Utils.NAN:
                error = "Duration n'est pas un nombre valide!\n"
                bot.isWorking = False
                return error + await usage(), None

        # Try to get an URL 5 times
        for _ in range(5):
            try:
                return await generateMap(bot, message, bot.driver, url, duration)
            except Exception as _:
                pass

        # If no URL could be generated, return usage
        error = "Une erreur tierce semble s'être produite.\n"
        bot.isWorking = False
        return error + await usage(), None

command = Command.Command()
command.name = "GENERATE"
command.emojis = [ac, acc]
command.activation = "!!generate"
command.nbArgs = [2, 3]
command.usage = usage
command.handle = handle
