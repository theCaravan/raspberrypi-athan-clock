"""Main Program"""
import time
import requests
import json
from unicornhatmini import UnicornHATMini
from constants import *

# Prayer Times Parameters
latitude = LOCATION[0]
longitude = LOCATION[1]
method = LOCATION[2]

# Initialize Unicorn Hat Mini
unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(SCREEN_BRIGHTNESS)

# Set none of the buttons as pressed
b_is_pressed_next_prayer = False
a_is_pressed_hijri_date = False
y_is_pressed_already_prayed = False
x_is_pressed_hide_time = False

initial_run = True

prayer_times_raw = {}
prayer_times_date = ""
upcoming_prayer_time = ""
hijri_date_raw = ""


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


def display_number(number, x_offset, y_offset, clear=False, rgb=None):
    """Display a single number"""
    if rgb is None:
        rgb = COLORS["white"]

    if clear:
        unicornhatmini.clear()

    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]

    for pixel in NUMBERS_TO_DRAW[number]:
        unicornhatmini.set_pixel(pixel[0] + x_offset, pixel[1] + y_offset, red, green, blue)
        unicornhatmini.show()
        time.sleep(TIME_DELAY)


def get_prayer_times(unix_time, lat, long, method_of_calculation):
    """Grab the prayer times from an API and return the values we can use later"""
    url_link = "{}/{}?latitude={}&longitude={}&method={}"\
        .format(API_INITIAL_LINK, unix_time, lat, long, method_of_calculation)

    r = requests.get(url=url_link)

    if r.status_code >= 400:
        print("{} URL related to {} returned this response: {} - {}".format(url_link, "Athan", r, r.text))

    return json.loads(r.text)


def pressed_b_next_prayer():
    """Show the next prayer time (or back to clock) when pressing the B (upper left) button on the Unicorn Hat Mini"""
    global b_is_pressed_next_prayer
    global initial_run

    if b_is_pressed_next_prayer:
        b_is_pressed_next_prayer = False
        unicornhatmini.clear()
        unicornhatmini.show()
        initial_run = True

    else:
        b_is_pressed_next_prayer = True


def pressed_a_hijri_date():
    """Show the Hijri date (or back to clock) when pressing the A (upper right) button on the Unicorn Hat Mini"""
    global a_is_pressed_hijri_date
    global initial_run

    if a_is_pressed_hijri_date:
        a_is_pressed_hijri_date = False
        unicornhatmini.clear()
        unicornhatmini.show()
        initial_run = True
    else:
        a_is_pressed_hijri_date = True


def pressed_y_already_prayed():
    """Hide/Show the Athan Snake when pressing the Y (bottom left) button on the Unicorn Hat Mini"""
    global y_is_pressed_already_prayed

    if y_is_pressed_already_prayed:
        y_is_pressed_already_prayed = False
    else:
        y_is_pressed_already_prayed = True


def pressed_x_hide_time():
    """Hide/Show the clock when pressing the X (bottom right) button on the Unicorn Hat Mini"""
    global x_is_pressed_hide_time

    if x_is_pressed_hide_time:
        x_is_pressed_hide_time = False
    else:
        x_is_pressed_hide_time = True


while True:
    # Time values are grabbed here
    if not MOCK_RUN:
        datetime_now = datetime.now()
    else:
        datetime_now = MOCK_DATETIME

    current_unix_time = int(time.mktime(datetime_now.timetuple()))
    today_date_str = datetime_now.strftime("%d/%m/%Y")

    BUTTON_B.when_pressed = pressed_b_next_prayer
    BUTTON_A.when_pressed = pressed_a_hijri_date
    BUTTON_Y.when_pressed = pressed_y_already_prayed
    BUTTON_X.when_pressed = pressed_x_hide_time

    # clear prayer times
    clear_section(12, 16, 0, 6)

    if x_is_pressed_hide_time:
        a_is_pressed_hijri_date = False
        b_is_pressed_next_prayer = False
        initial_run = True

        time.sleep(TIME_DELAY)
        unicornhatmini.clear()

        unicornhatmini.show()
        continue

    # Grab current prayer time
    if b_is_pressed_next_prayer:
        a_is_pressed_hijri_date = False
        x_is_pressed_hide_time = False
        initial_run = True

        time.sleep(TIME_DELAY)
        unicornhatmini.clear()

        if upcoming_prayer_time != 0:
            hour = upcoming_prayer_time.split(":")[0]
            minute = upcoming_prayer_time.split(":")[1]
        else:
            b_is_pressed_next_prayer = False
            continue

    elif a_is_pressed_hijri_date:
        b_is_pressed_next_prayer = False
        x_is_pressed_hide_time = False
        initial_run = True

        time.sleep(TIME_DELAY)
        unicornhatmini.clear()

        hour = hijri_date_raw.split("/")[0]
        minute = hijri_date_raw.split("/")[1]

    else:
        hour = datetime_now.strftime("%H")
        minute = datetime_now.strftime("%M")

    # Only run this at the first run and
    # at the first minute of the hour (i.e. 10:00, 12:00)
    if int(minute) == 0 or initial_run:
        # Clear the entire hours row
        clear_section(0, 4, 0, 6)

        # Double Digit Hour
        if len(hour) == 2:
            hour_tens = int(hour[0])
            hour_ones = int(hour[1])

            display_number(hour_tens, 0, 0)
            display_number(hour_ones, 0, -4)

        # Single Digit Hour
        else:
            hour_tens = 0
            hour_ones = int(hour)
            display_number(hour_ones, 0, -2)

        initial_run = False

    if int(minute) in [0, 10, 20, 30, 40, 50]:
        # Clear the entire minutes section
        clear_section(6, 10, 0, 6)
    else:
        # Clear just the ones minutes section
        clear_section(6, 10, 0, 2)

    if len(minute) == 2:
        minute_tens = int(minute[0])
        minute_ones = int(minute[1])
    else:
        minute_tens = 0
        minute_ones = int(minute)

    display_number(minute_tens, 6, 0)
    display_number(minute_ones, 6, -4)

    # Only grab this if we didn't have them stored or if it's the wrong day
    if prayer_times_raw == {} or prayer_times_date == "" or prayer_times_date != today_date_str:
        raw_request = get_prayer_times(current_unix_time, latitude, longitude, method)
        prayer_times_raw = raw_request["data"]["timings"]
        hijri_date_raw = "{}/{}".format(raw_request["data"]["date"]["hijri"]["month"]["number"],
                                        raw_request["data"]["date"]["hijri"]["day"])

    # Grab all the prayer times from the keys, excluding Sunset, Imsak, Midnight, Firstthird, Lastthird
    prayer_times = []
    for prayer_time in prayer_times_raw.keys():

        prayer_times_date = today_date_str

        if prayer_time in ["Sunset", "Imsak", "Midnight", "Firstthird", "Lastthird"]:
            continue

        prayer_time_today = "{} {}".format(
            prayer_times_date,
            prayer_times_raw[prayer_time]
        )

        prayer_times.append(datetime.strptime(prayer_time_today, "%d/%m/%Y %H:%M"))

    # Compare the times to right now and see how close we are to the next time:
    right_now = datetime.strptime("{} {}:{}".format(prayer_times_date, hour, minute), "%d/%m/%Y %H:%M")

    differences_in_minutes = []
    next_prayer_time_name = ""
    next_prayer_time_minutes = 0

    index = 0
    recent_difference = 0
    for prayer_time in prayer_times:
        difference = (prayer_time - right_now).total_seconds() / 60

        # only focus on the closest one greater than zero
        if difference > 0:
            next_prayer_time_minutes = int(difference)
            next_prayer_time_name = PRAYER_INDEXES[index]
            break

        recent_difference = 0 - difference
        index += 1

    if not b_is_pressed_next_prayer:
        try:
            upcoming_prayer_time = prayer_times_raw[next_prayer_time_name]
        except KeyError:
            upcoming_prayer_time = 0
            y_is_pressed_already_prayed = True

    # take the length of the prayer time
    prayer_length = recent_difference + next_prayer_time_minutes

    if 0 <= recent_difference <= 2:
        y_is_pressed_already_prayed = False

    # convert to a percentage and display on bar graph
    if prayer_length != 0:
        percent_remaining = int(round(100 * (next_prayer_time_minutes / prayer_length)))
    else:
        percent_remaining = 0

    if next_prayer_time_name not in ["Fajr", "Dhuhr"] \
            and not y_is_pressed_already_prayed\
            and percent_remaining != 0:
        display_snake_pct(percent_remaining)

    t = datetime.utcnow()
    sleep_time = 60 - t.second
    for i in range(sleep_time * 20):
        saved_b_next_prayer = b_is_pressed_next_prayer
        saved_a_hijri_date = a_is_pressed_hijri_date
        saved_y_already_prayed = y_is_pressed_already_prayed
        saved_x_hide_time = x_is_pressed_hide_time

        time.sleep(TIME_DELAY)
        if saved_x_hide_time != x_is_pressed_hide_time or saved_y_already_prayed != y_is_pressed_already_prayed\
                or saved_a_hijri_date != a_is_pressed_hijri_date or saved_b_next_prayer != b_is_pressed_next_prayer:
            break
