import time, os

import Utils
import Command

from CommandReturn import CommandReturn, ErrorType

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
xpath_challenge = "/html/body/div/div/main/div/div/div/div/div/div/article/div[2]/div/div[2]/label/div[1]"
xpath_settings = "/html/body/div/div/main/div/div/div/div/div/div/article/div[3]/div/div/div/label/span[3]"
xpath_move = "/html/body/div/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[1]/span"
xpath_no_move = "/html/body/div/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[2]/span"
xpath_time = "/html/body/div/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[2]/div[2]"
xpath_inviteFriends = "/html/body/div/div/main/div/div/div/div/div/div/article/div[4]/button"
xpath_URL = "/html/body/div/div/main/div/div/div/div/div/div/article/div[2]/div/section/article/span/input"

xpath_country_challenge = "/html/body/div/div/main/div/div/div/div/div/div/div[2]/article/div[2]/div/div[2]/label/div[1]"
xpath_country_settings = "/html/body/div/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[1]/label/span[1]"
xpath_country_move = "/html/body/div/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[1]/span"
xpath_country_no_move = "/html/body/div/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[2]/span"
xpath_country_time = "/html/body/div/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[2]/div[2]"
xpath_country_inviteFriends = "/html/body/div/div/main/div/div/div/div/div/div/div[2]/article/div[4]/button"
xpath_country_URL = "/html/body/div/div/main/div/div/div/div/div/div/div[2]/article/div[2]/div/section/article/span/input"

# The time slider factor : 8 to the right = 10 seconds
shift = 4.9

# Emojis (help display)
acc = ":arrows_counterclockwise:"
ac = ":arrows_clockwise:"

# url for country streak
url_cs = "https://www.geoguessr.com/country-streak"

# true strings
true_strings = [
    "true",
    "t",
    "y",
    "yes",
    "Yes",
    "Y",
    "T",
    "True",
    "Oui",
    "O",
    "1",
    "V",
    "v",
    "Vrai",
    "vrai"
]

no_move_strings = [
    "nm",
    "no-move",
    "no-mv",
    "nmv"
]

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Génère un challenge pour une map spécifiée.\n"
    msg += "`!!generate <map_url> [duration] [no-move]`\n"
    msg += "`map_url`: Url vers la map à générer (peut aussi être un shortcut).\n"
    msg += "`duration` (opt): Durée d'un round en secondes ou au format min:sec.\n"
    msg += "`no-move` (opt): True (ou un alias valide) pour jouer en no move.\n"
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
    time.sleep(4)

    # Log in with google
    driver.find_element(By.XPATH, xpath_google).click()
    time.sleep(2)
    
    # If everything is working fine, a new window has been opened
    if len(driver.window_handles) > 1:

        # Log in
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element(By.XPATH, xpath_mail).send_keys(mail)
        driver.find_element(By.XPATH, xpath_mailNext).click()

        time.sleep(3)
        driver.find_element(By.XPATH, xpath_password).send_keys(password)
        driver.find_element(By.XPATH, xpath_passwordNext).click()
        driver.switch_to.window(driver.window_handles[0])

        # Required wait (going too fast breaks selenium)
        time.sleep(10)

async def setupChallenge(driver, duration, no_move):
    # Click on the play button
    driver.find_element(By.XPATH, xpath_play).click()
    time.sleep(2)

    # Click on the challenge button
    driver.find_element(By.XPATH, xpath_challenge).click()
    time.sleep(2)

    # Have settings been clicked already?
    try:
        driver.find_element(By.XPATH, xpath_no_move)
    except Exception as _:
        # Click settings 
        driver.find_element(By.XPATH, xpath_settings).click()
    time.sleep(2)

    # No move
    if no_move:
        driver.find_element(By.XPATH, xpath_no_move).click()

    else:
        driver.find_element(By.XPATH, xpath_move).click()
    
    time.sleep(2)

    # Slide to the correct duration
    slider = driver.find_element(By.XPATH, xpath_time)
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(-100, 0).release().perform()
    move.click_and_hold(slider).move_by_offset(int(duration / 10) * shift, 0).release().perform()
    time.sleep(2)

    # Get to the URL of the challenge
    driver.find_element(By.XPATH, xpath_inviteFriends).click()
    time.sleep(2)

async def setupChallengeCountry(driver, duration, no_move):

    # Click on the challenge button
    driver.find_element(By.XPATH, xpath_country_challenge).click()
    time.sleep(1)

    # Have settings been clicked already?
    try:
        driver.find_element(By.XPATH, xpath_country_no_move)
    except Exception as _:
        # Click settings 
        driver.find_element(By.XPATH, xpath_country_settings).click()
        time.sleep(0.5)

    # No move
    if no_move:
        driver.find_element(By.XPATH, xpath_country_no_move).click()
        time.sleep(1)

    else:
        driver.find_element(By.XPATH, xpath_country_move).click()
        time.sleep(1)

    # Slide to the correct duration
    slider = driver.find_element(By.XPATH, xpath_country_time)
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(-100, 0).release().perform()
    move.click_and_hold(slider).move_by_offset(int(duration / 10) * shift, 0).release().perform()
    time.sleep(2)

    # Get to the URL of the challenge
    driver.find_element(By.XPATH, xpath_country_inviteFriends).click()
    time.sleep(1)

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
async def generateMap(bot, message, driver, url, duration, no_move):
    country = False

    if url == "Country":
        country = True

    # If the URL is not valid
    elif not await Utils.isValidURL(url):
        error = "L'URL n'est pas valide!\n"
        return CommandReturn(error + await usage(), None, ErrorType.UrlError)

    # Go to the URL
    if not country:
        driver.get(url)
    else:
        driver.get(url_cs)
    time.sleep(2)

    # If the bot is not logged in
    if not await isLogged(driver):
        await log(driver)
        driver.get(url)
        time.sleep(2)
    
    title = None
    # Get the name of the map to generate
    if not country:
        title = await getTitle(driver)
        if title == None:
            error = "L'URL ne pointe pas vers une map GeoGuessr!\n"
            return CommandReturn(error + await usage(), None, ErrorType.NotAMapError)
    else:
        title = "Country Streak"

    time.sleep(2)

    # Round the duration to a valid number of seconds
    duration = await roundDuration(duration)

    # Setup the challenge
    if not country:
        await setupChallenge(driver, duration, no_move)
    else:
        await setupChallengeCountry(driver, duration, no_move)

    msg = title
    if not country:
        challenge = "<" + driver.find_element(By.XPATH, xpath_URL).get_attribute('value') + ">"
    else:
        challenge = "<" + driver.find_element(By.XPATH, xpath_country_URL).get_attribute('value') + ">"
    msg += ": " + challenge

    if duration == 0:
        duration = "temps illimité!"
        msg += " " + duration
    else:
        msg += " " + str(duration) + " secondes par rounds!"

    if no_move:
        msg += " (no move)"

    bot.archives.add({"title": title, "who": str(message.author), "duration":str(duration), "url":challenge})

    return CommandReturn(msg)

async def handle(bot, command, message, content):
    try:
        if bot.isWorking == False:
            bot.isWorking = True

            # Get the URL
            url = content[1]

            if url in bot.shortcuts:
                url = bot.shortcuts[url]["url"]

            duration = 0
            no_move = False

            # Get the duration (if specified)
            if len(content) >= 3:
                duration = await Utils.timeToInt(content[2])
                if duration == Utils.NAN:
                    error = "Duration n'est pas un nombre valide!\n"
                    bot.isWorking = False
                    return CommandReturn(error + await usage(), None, ErrorType.DurationError)

            if len(content) >= 4:
                no_move_cont = content[3]
                if no_move_cont in true_strings or no_move_cont in no_move_strings:
                    no_move = True

            # Try to get an URL 5 times
            for _ in range(5):
                try:
                    res = await generateMap(bot, message, bot.driver, url, duration, no_move)
                    if res.error == None:
                        bot.isWorking = False
                        return res
                except Exception as e:
                    print(e)

            # If no URL could be generated, return usage
            error = "Une erreur tierce semble s'être produite.\n"
            bot.isWorking = False
            return CommandReturn(error + await usage(), None, ErrorType.UnknownError)
    except Exception as e:
        return CommandReturn(str(e), None, ErrorType.UnknownError)
    
    return CommandReturn("Bot is working!", None, ErrorType.BusyBotError)

command = Command.Command()
command.name = "GENERATE"
command.emojis = [ac, acc]
command.activation = "!!generate"
command.nbArgs = [2, 4]
command.usage = usage
command.handle = handle
