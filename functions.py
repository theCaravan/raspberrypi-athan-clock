"""Define the functions used in this project"""
import json
import requests

from adjustable_settings import TIME_DELAY
from constants import (SNAKE_COORDINATES,
                       COLORS,
                       NUMBERS_TO_DRAW,
                       API_INITIAL_LINK,
                       )
from mock_hat_mini.bridge import set_pixel as hat_set_pixel
from mock_hat_mini.bridge import sleep as hat_sleep
from mock_hat_mini.bridge import show as hat_show
from mock_hat_mini.bridge import clear as hat_clear


def clear_section(start_x, end_x, start_y, end_y) -> None:
    """Clear a section of pixels, such as when changing the number or an entire line for a new
    hour"""
    this_x = start_x

    if start_x > end_x:
        print("Error, cannot clear section as start_x: {} is greater than end_x: {}".format(start_x,
                                                                                            end_x
                                                                                            )
              )

    if start_y > end_y:
        print("Error, cannot clear section as start_y: {} is greater than end_y: {}".format(start_y,
                                                                                            end_y
                                                                                            )
              )

    while this_x <= end_x:
        this_y = start_y
        while this_y <= end_y:
            hat_set_pixel(this_x, this_y, 0, 0, 0)
            this_y += 1
        this_x += 1

    hat_sleep(TIME_DELAY)
    hat_show()


def display_snake_pct(percent) -> None:
    """Display the remaining percentage based on the coordinates and colors set by
    SNAKE_COORDINATES"""
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

        hat_sleep(TIME_DELAY)
        hat_set_pixel(x, y, r, g, b)
        hat_show()


def display_number(number, x_offset, y_offset, clear = False, rgb = None, test = False) -> None:
    """Display a single number"""
    if rgb is None:
        rgb = COLORS["white"]

    if clear or test:
        hat_clear()

    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]

    for pixel in NUMBERS_TO_DRAW[number]:
        hat_set_pixel(pixel[0] + x_offset, pixel[1] + y_offset, red, green, blue)

        # Show the same number 6 times to ensure the display is working on test mode
        if test:
            hat_set_pixel(pixel[0] + x_offset + 6, pixel[1] + y_offset, red, green, blue)
            hat_set_pixel(pixel[0] + x_offset - 5, pixel[1] + y_offset, red, green, blue)
            hat_set_pixel(pixel[0] + x_offset, pixel[1] + y_offset - 4, red, green, blue)
            hat_set_pixel(pixel[0] + x_offset + 6,
                          pixel[1] + y_offset - 4,
                          red,
                          green,
                          blue
                          )
            hat_set_pixel(pixel[0] + x_offset - 5,
                          pixel[1] + y_offset - 4,
                          red,
                          green,
                          blue
                          )

        hat_show()
        hat_sleep(TIME_DELAY)


def get_prayer_times(unix_time, lat, long, method_of_calculation) -> dict:
    """Grab the prayer times from an API and return the values we can use later"""
    url_link = "{}/{}?latitude={}&longitude={}&method={}" \
        .format(API_INITIAL_LINK, unix_time, lat, long, method_of_calculation)

    r = requests.get(url = url_link)

    return {
        "result": "success",
        "r.text": json.loads(r.text),
        }


def test_numbers() -> None:
    """Initial run of the clock to show you the numbers and to verify it all works"""
    current_number = 9
    while current_number >= 0:
        display_number(current_number, 0, 0, test = True)
        hat_sleep(TIME_DELAY * 2)
        current_number -= 1
    hat_clear()


def display_snake_error() -> None:
    """Display error in the snake area"""
    for percentage in [89, 74, 60, 46, 31, 17, 3]:
        x = SNAKE_COORDINATES[percentage][0][0]
        y = SNAKE_COORDINATES[percentage][0][1]

        r = COLORS["red"][0]
        g = COLORS["red"][1]
        b = COLORS["red"][2]

        hat_sleep(TIME_DELAY)
        hat_set_pixel(x, y, r, g, b)
        hat_show()
