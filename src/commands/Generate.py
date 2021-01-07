import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.utils.Utils as Utils
import src.commands.Command as Command

from src.commands.CommandReturn import CommandReturn, ErrorType

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

###################################################################################################
###################################### VARIABLES ##################################################
###################################################################################################

# XPATH LIST
xpath_play = "/html/body/div/div/main/div/div/div[1]/div[3]/button"
xpath_play_bis = "/html/body/div/div/main/div/div/div[1]/div[4]/button"
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

max_timeout = 5

duration_flag = "-d"
no_move_flag = "-n"

###################################################################################################
###################################### METHODS ####################################################
###################################################################################################

async def usage():
    msg = "Generates a challenge for a given map.\n"
    msg += "`!!generate <map_url> [-d duration] [-n]`\n"
    msg += "`map_url`: Url or shortcut of a map.\n"
    msg += "`-d [duration]` (opt): Duration of a round min:sec (unlimited by default).\n"
    msg += "`-n` (opt): If set, no movement will be allowed.\n\n"
    msg += "Example: `!!generate https://www.geoguessr.com/maps/world`\n"
    msg += "Example: `!!generate -d 1:20 https://www.geoguessr.com/maps/world`\n"
    msg += "Example: `!!generate -d 3:00 https://www.geoguessr.com/maps/world -n`\n"
    return msg

async def setup_challenge(driver, duration, no_move):
    # Click on the play button
    try:
        Utils.get_element(driver, xpath_play, 1).click()
    except Exception as _:
        time.sleep(1)
        Utils.get_element(driver, xpath_play_bis, 1).click()

    # Click on the challenge button
    Utils.get_element(driver, xpath_challenge).click()

    # Have settings been clicked already?
    try:
        driver.find_element(By.XPATH, xpath_no_move)
    except Exception as _:
        # Click settings 
        Utils.get_element(driver, xpath_settings).click()

    # No move
    if no_move:
        Utils.get_element(driver, xpath_no_move).click()

    else:
        Utils.get_element(driver, xpath_move).click()

    # Slide to the correct duration
    slider = Utils.get_element(driver, xpath_time)
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(-100, 0).release().perform()
    move.click_and_hold(slider).move_by_offset(int(duration / 10) * shift, 0).release().perform()

    # Get to the URL of the challenge
    Utils.get_element(driver, xpath_inviteFriends).click()

async def setup_challenge_country(driver, duration, no_move):

    # Click on the challenge button
    Utils.get_element(driver, xpath_country_challenge).click()

    # Have settings been clicked already?
    try:
        driver.find_element(By.XPATH, xpath_country_no_move)
    except Exception as _:
        # Click settings 
        Utils.get_element(driver, xpath_country_settings).click()

    # No move
    if no_move:
        Utils.get_element(driver, xpath_country_no_move).click()

    else:
        Utils.get_element(driver, xpath_country_move).click()

    # Slide to the correct duration
    slider = Utils.get_element(driver, xpath_country_time)
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(-100, 0).release().perform()
    move.click_and_hold(slider).move_by_offset(int(duration / 10) * shift, 0).release().perform()

    # Get to the URL of the challenge
    Utils.get_element(driver, xpath_country_inviteFriends).click()

async def round_duration(duration):
    # Max is 600, min is 0
    if duration > 600 or duration <= 0:
        return 0

    return int(duration / 10) * 10

async def get_title(driver):
    try:
        return await Utils.get_title(driver)
    except Exception as _:
        pass
    return None

# Generates a URL to a challenge with a set duration
async def generate_map(bot, message, driver, url, duration, no_move):
    country = False

    if url == "Country":
        country = True

    # If the URL is not valid
    elif not await Utils.is_valid_url(url):
        error = "Invalid URL!\n"
        return CommandReturn(error + await usage(), None, ErrorType.UrlError)

    # Go to the URL
    if not country:
        driver.get(url)
    else:
        driver.get(url_cs)

    # If the bot is not logged in
    if not await Utils.is_logged(driver):
        await Utils.log(driver)
        driver.get(url)
    
    title = None
    # Get the name of the map to generate
    if not country:
        title = await get_title(driver)
        if title == None:
            error = "This URL does not lead to a Geoguessr map!\n"
            return CommandReturn(error + await usage(), None, ErrorType.NotAMapError)
    else:
        title = "Country Streak"

    # Round the duration to a valid number of seconds
    duration = await round_duration(duration)

    # Setup the challenge
    if not country:
        await setup_challenge(driver, duration, no_move)
    else:
        await setup_challenge_country(driver, duration, no_move)

    # creating the message to return
    msg = title
    if not country:
        challenge = "<" +Utils.get_element(driver, xpath_URL).get_attribute('value') + ">"
    else:
        challenge = "<" + Utils.get_element(driver, xpath_country_URL).get_attribute('value') + ">"
    msg += ": " + challenge

    if duration == 0:
        duration = "unlimited time!"
        msg += " " + duration
    else:
        msg += " " + await Utils.int_to_time(duration) + " per rounds!"

    if no_move:
        msg += " (no move)"

    bot.archives.add({"title": title, "who": str(message.author), "duration":str(duration), "url":challenge})

    return CommandReturn(msg)

async def handle(bot, command, message, arguments):

    # try block in case something goes awfully wrong
    try:

        # if the bot is already doing something, don't try to generate another map
        if bot.is_working == False:

            # true bc the bot is now working
            bot.is_working = True

            # Get the URL from the first positional argument
            url = arguments.get_pos(0)

            # get the url if the given "url" is actually a shortcut
            if url in bot.shortcuts:
                url = bot.shortcuts[url]["url"]

            # duration of the round
            duration = 0

            # no move?
            no_move = False

            # Get the duration (if specified)
            if arguments.is_flag_set(duration_flag):

                # get the duration from the non positional flag
                duration = await Utils.time_to_int(arguments.get_non_pos(duration_flag)[0])

                # if the duration is invalid, abort
                if duration == Utils.NAN:
                    error = "The given duration is invalid!\n"
                    bot.is_working = False
                    return CommandReturn(error + await usage(), None, ErrorType.DurationError)

            # get the no_move value (if specified)
            if arguments.is_flag_set(no_move_flag):
                no_move = True

            # Try to get an URL 5 times (sometimes if the bot goes to fast it may
            # not work on the first try)
            for _ in range(5):

                # try block in case something goes wrong
                try:

                    # generate the map (hopefully)
                    res = await generate_map(bot, message, bot.driver, url, duration, no_move)

                    # if no error is detected, or this is one of the following, everything is fine
                    if res.error == None or res.error == ErrorType.NotAMapError or res.error == ErrorType.UrlError:
                        bot.is_working = False
                        return res

                except Exception as e:
                    pass
                    # print(e)

            # If no URL could be generated, return usage
            # this hopefully is never reached
            error = "Something went awfully wrong!\n"
            bot.is_working = False
            return CommandReturn(error + await usage(), None, ErrorType.UnknownError)

    # this should also never happen...
    except Exception as e:
        bot.is_working = False
        return CommandReturn(str(e), None, ErrorType.UnknownError)
    
    # if the bot is already doing something
    return CommandReturn("Bot is busy!", None, ErrorType.BusyBotError)

command = Command.Command()
command.name = "GENERATE"
command.emojis = [ac, acc]
command.activation = "!!generate"
command.usage = usage
command.handle = handle
command.expected_pos = 1

# duration flag
command.flags.add_flag(duration_flag, 1)

# no-move flag
command.flags.add_flag(no_move_flag, 0)