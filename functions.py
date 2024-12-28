"""Define the functions used in this project"""
import os
import time
import json
import requests
from unicornhatmini import UnicornHATMini
import slack_sdk
from constants import *

# Initialize Unicorn Hat Mini
unicornhatmini = UnicornHATMini()


def post_to_slack(slack_channel, post_text, slack_api_key, mock_run):
    """Post text to Slack. If mock_run = True, print the text here instead"""

    if mock_run:
        print("--- post_to_slack: This would have posted to Slack Channel '{}' ---".format(slack_channel))
        print(post_text)
        print("--- post_to_slack: End ---")
        return

    client = slack_sdk.WebClient(os.environ[slack_api_key])
    response = client.chat_postMessage(channel=slack_channel,
                                       text=post_text)
    return response


def clear_section(start_x, end_x, start_y, end_y):
    """Clear a section of pixels, such as when changing the number or an entire line for a new hour"""
    this_x = start_x

    if start_x > end_x:
        print("Error, cannot clear section as start_x: {} is greater than end_x: {}".format(start_x, end_x))

    if start_y > end_y:
        print("Error, cannot clear section as start_y: {} is greater than end_y: {}".format(start_y, end_y))

    while this_x <= end_x:
        this_y = start_y
        while this_y <= end_y:
            unicornhatmini.set_pixel(this_x, this_y, 0, 0, 0)
            this_y += 1
        this_x += 1

    time.sleep(TIME_DELAY)
    unicornhatmini.show()


def display_snake_pct(percent):
    """Display the remaining percentage based on the coordinates and colors set by SNAKE_COORDINATES"""
    percent = int(percent)

    if percent > 100 or percent < 0:
        raise ValueError

    percentages = SNAKE_COORDINATES.keys()

    # Grab the percentage value just greater than the last, which was less than or equal
    previous_percentage = 0
    for percentage in percentages:
        if percent >= percentage:
            break
        previous_percentage = percentage

    if percent == 100:
        previous_percentage = 100

    percent = previous_percentage

    # List all except ones way greater than this percent
    percentages_to_display = []
    for percentage in percentages:
        if percent >= percentage:
            percentages_to_display.append(percentage)

    for percentage in percentages_to_display:
        x = SNAKE_COORDINATES[percentage][0][0]
        y = SNAKE_COORDINATES[percentage][0][1]

        r = SNAKE_COORDINATES[percentage][1][0]
        g = SNAKE_COORDINATES[percentage][1][1]
        b = SNAKE_COORDINATES[percentage][1][2]

        time.sleep(TIME_DELAY)
        unicornhatmini.set_pixel(x, y, r, g, b)
        unicornhatmini.show()


def display_number(number, x_offset, y_offset, clear=False, rgb=None, test=False):
    """Display a single number"""
    if rgb is None:
        rgb = COLORS["white"]

    if clear or test:
        unicornhatmini.clear()

    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]

    for pixel in NUMBERS_TO_DRAW[number]:
        unicornhatmini.set_pixel(pixel[0] + x_offset, pixel[1] + y_offset, red, green, blue)

        # Show the same number 6 times to ensure the display is working on test mode
        if test:
            unicornhatmini.set_pixel(pixel[0] + x_offset + 6, pixel[1] + y_offset, red, green, blue)
            unicornhatmini.set_pixel(pixel[0] + x_offset - 5, pixel[1] + y_offset, red, green, blue)
            unicornhatmini.set_pixel(pixel[0] + x_offset, pixel[1] + y_offset - 4, red, green, blue)
            unicornhatmini.set_pixel(pixel[0] + x_offset + 6, pixel[1] + y_offset - 4, red, green, blue)
            unicornhatmini.set_pixel(pixel[0] + x_offset - 5, pixel[1] + y_offset - 4, red, green, blue)

        unicornhatmini.show()
        time.sleep(TIME_DELAY)


def get_prayer_times(unix_time, lat, long, method_of_calculation):
    """Grab the prayer times from an API and return the values we can use later"""
    url_link = "{}/{}?latitude={}&longitude={}&method={}"\
        .format(API_INITIAL_LINK, unix_time, lat, long, method_of_calculation)

    r = requests.get(url=url_link)

    if r.status_code >= 400:
        send_to_slack = "{} URL related to {} returned this response: {} - {}".format(url_link, "Athan", r, r.text)
        post_to_slack(MOCK_SLACK_CHANNEL, send_to_slack, SLACK_API_KEY, MOCK_RUN)

        return {
            "result": "error",
            "error": send_to_slack,
            "website": url_link,
        }

    return {
        "result": "success",
        "r.text": json.loads(r.text),
    }


def test_numbers():
    """Initial run of the clock to show you the numbers and to verify it all works"""
    current_number = 9
    while current_number >= 0:
        display_number(current_number, 0, 0, test=True)
        time.sleep(TIME_DELAY * 2)
        current_number -= 1
    unicornhatmini.clear()


def display_snake_error():
    """Display error in the snake area"""
    for percentage in [89, 74, 60, 46, 31, 17, 0]:
        x = SNAKE_COORDINATES[percentage][0][0]
        y = SNAKE_COORDINATES[percentage][0][1]

        r = COLORS["red"][0]
        g = COLORS["red"][1]
        b = COLORS["red"][2]

        time.sleep(TIME_DELAY)
        unicornhatmini.set_pixel(x, y, r, g, b)
        unicornhatmini.show()
