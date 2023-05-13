import time
import requests
import json
from datetime import datetime
from datetime import date
from unicornhatmini import UnicornHATMini
from gpiozero import Button

# Prayer Times Parameters
locations = {
    "Maplewood": [45.031553, -93.024759, 2]
}

current_location = "Maplewood"

latitude = locations[current_location][0]
longitude = locations[current_location][1]
method = locations[current_location][2]

unicornhatmini = UnicornHATMini()

unicornhatmini.set_brightness(0.1)

# Note, this is aligned to the top and left
numbers = {
    0: [
        [0, 6], [0, 5], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [4, 5], [4, 6], [3, 6], [2, 6], [1, 6]
    ],

    1: [
        [1, 6], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [4, 6], [4, 4]
    ],

    2: [
        [0, 6], [0, 5], [0, 4], [1, 4], [2, 4], [2, 5], [2, 6], [3, 6], [4, 6], [4, 5], [4, 4]
    ],

    3: [
        [0, 6], [0, 5], [0, 4], [1, 4], [2, 4], [2, 5], [2, 6], [3, 4], [4, 4], [4, 5], [4, 6]
    ],

    4: [
        [0, 6], [1, 6], [2, 6], [2, 5], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4]
    ],

    5: [
        [0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [2, 5], [2, 4], [3, 4], [4, 4], [4, 5], [4, 6]
    ],

    6: [
        [0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [3, 6], [4, 6], [4, 5], [4, 4], [3, 4], [2, 4], [2, 5]
    ],

    7: [
        [0, 6], [0, 5], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4]
    ],

    8: [
        [1, 6], [0, 6], [0, 5], [0, 4], [1, 4], [2, 4], [2, 5], [2, 6], [3, 6], [4, 6], [4, 5], [4, 4], [3, 4]
    ],

    9: [
        [2, 5], [2, 6], [1, 6], [0, 6], [0, 5], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [4, 5], [4, 6]
    ]
}

already_prayed = False

button_x = Button(16)
button_y = Button(24)
button_b = Button(6)
button_a = Button(5)

snake = {
    100: [[12, 6], [255, 255, 255]],
    97: [[13, 6], [255, 255, 255]],
    94: [[14, 6], [255, 255, 255]],
    91: [[15, 6], [255, 255, 255]],
    89: [[16, 6], [255, 255, 255]],
    86: [[12, 5], [0, 255, 255]],
    83: [[13, 5], [0, 255, 255]],
    80: [[14, 5], [0, 255, 255]],
    77: [[15, 5], [0, 255, 255]],
    74: [[16, 5], [0, 255, 255]],
    71: [[12, 4], [0, 255, 0]],
    69: [[13, 4], [0, 255, 0]],
    66: [[14, 4], [0, 255, 0]],
    63: [[15, 4], [0, 255, 0]],
    60: [[16, 4], [0, 255, 0]],
    57: [[12, 3], [255, 255, 0]],
    54: [[13, 3], [255, 255, 0]],
    51: [[14, 3], [255, 255, 0]],
    49: [[15, 3], [255, 255, 0]],
    46: [[16, 3], [255, 255, 0]],
    43: [[12, 2], [255, 153, 0]],
    40: [[13, 2], [255, 153, 0]],
    37: [[14, 2], [255, 153, 0]],
    34: [[15, 2], [255, 153, 0]],
    31: [[16, 2], [255, 153, 0]],
    29: [[12, 1], [255, 0, 0]],
    26: [[13, 1], [255, 0, 0]],
    23: [[14, 1], [255, 0, 0]],
    20: [[15, 1], [255, 0, 0]],
    17: [[16, 1], [255, 0, 0]],
    14: [[12, 0], [255, 0, 255]],
    11: [[13, 0], [255, 0, 255]],
    9: [[14, 0], [255, 0, 255]],
    6: [[15, 0], [255, 0, 255]],
    3: [[16, 0], [255, 0, 255]]
}

# What happens when button X is pressed
hide_time = False

a_is_pressed = False
b_is_pressed = False

start_time = time.time()
initial_run = True

prayer_times_raw = {}
prayer_times_date = ""
upcoming_prayer_time = ""
hijri_date_raw = ""


def clear_section(start_x, end_x, start_y, end_y):
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

    time.sleep(0.05)
    unicornhatmini.show()


def display_snake_pct(percent, initial_run_snake):
    percent = int(percent)

    if percent > 100 or percent < 0:
        raise ValueError

    percentages = snake.keys()

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
        x = snake[percentage][0][0]
        y = snake[percentage][0][1]

        r = snake[percentage][1][0]
        g = snake[percentage][1][1]
        b = snake[percentage][1][2]

        time.sleep(0.05)
        unicornhatmini.set_pixel(x, y, r, g, b)
        unicornhatmini.show()


def display_number(number, x_offset=0, y_offset=0, clear=False, rgb=None):
    if rgb is None:
        rgb = [255, 255, 255]

    if clear:
        unicornhatmini.clear()

    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]

    for pixel in numbers[number]:
        unicornhatmini.set_pixel(pixel[0] + x_offset, pixel[1] + y_offset, red, green, blue)
        unicornhatmini.show()
        time.sleep(0.05)


def get_prayer_times(unix_time, lat, long, method_of_calculation):
    url_link = "http://api.aladhan.com/v1/timings/{}?latitude={}&longitude={}&method={}"\
        .format(unix_time, lat, long, method_of_calculation)

    r = requests.get(url=url_link)

    if r.status_code >= 400:
        print("{} URL related to {} returned this response: {} - {}".format(url_link, "Athan", r, r.text))

    return json.loads(r.text)


def pressed_x():
    global hide_time

    if hide_time:
        hide_time = False
    else:
        hide_time = True


def pressed_y():
    global already_prayed

    if already_prayed:
        already_prayed = False
    else:
        already_prayed = True


def pressed_a():
    global a_is_pressed
    global initial_run

    if a_is_pressed:
        a_is_pressed = False
        unicornhatmini.clear()
        unicornhatmini.show()
        initial_run = True
    else:
        a_is_pressed = True


def pressed_b():
    global b_is_pressed
    global initial_run

    if b_is_pressed:
        b_is_pressed = False
        unicornhatmini.clear()
        unicornhatmini.show()
        initial_run = True

    else:
        b_is_pressed = True


while True:
    button_x.when_pressed = pressed_x
    button_y.when_pressed = pressed_y
    button_b.when_pressed = pressed_b
    button_a.when_pressed = pressed_a

    # clear prayer times
    clear_section(12, 16, 0, 6)

    if hide_time:
        a_is_pressed = False
        b_is_pressed = False
        time.sleep(0.05)
        unicornhatmini.clear()
        unicornhatmini.show()
        initial_run = True
        continue

    # Grab current prayer time
    if b_is_pressed:
        a_is_pressed = False
        hide_time = False
        time.sleep(0.05)
        unicornhatmini.clear()
        hour = upcoming_prayer_time.split(":")[0]
        minute = upcoming_prayer_time.split(":")[1]
        initial_run = True

    elif a_is_pressed:
        b_is_pressed = False
        hide_time = False
        time.sleep(0.05)
        unicornhatmini.clear()
        hour = hijri_date_raw.split("/")[0]
        minute = hijri_date_raw.split("/")[1]
        initial_run = True

    else:
        hour = datetime.now().strftime("%H")
        minute = datetime.now().strftime("%M")

    # Only run this at the first run and
    # at the first minute of the hour (i.e. 10:00, 12:00)
    if int(minute) == 0 or initial_run:
        # Clear the entire hours row
        clear_section(0, 4, 0, 6)

        # Double Digit Hour
        if len(hour) == 2:
            hour_tens = int(hour[0])
            hour_ones = int(hour[1])

            display_number(hour_tens)
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

    display_number(minute_tens, 6)
    display_number(minute_ones, 6, -4)

    # Get the prayer times prepped
    current_unix_time = int(time.time())
    today_date_str = date.today().strftime("%d/%m/%Y")

    # Only grab this if we didn't have them stored or it's the wrong day
    if prayer_times_raw == {} or prayer_times_date == "" or prayer_times_date != today_date_str:
        raw_request = get_prayer_times(current_unix_time, latitude, longitude, method)
        prayer_times_raw = raw_request["data"]["timings"]
        hijri_date_raw = "{}/{}".format(raw_request["data"]["date"]["hijri"]["month"]["number"], raw_request["data"]["date"]["hijri"]["day"])

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

    differences_in_mins = []
    next_prayer_time_name = ""
    next_prayer_time_mins = 0

    index = 0
    recent_difference = 0
    prayer_indexes = {
        0: "Fajr",
        1: "Sunrise",
        2: "Dhuhr",
        3: "Asr",
        4: "Maghrib",
        5: "Isha"
    }
    for prayer_time in prayer_times:
        difference = (prayer_time - right_now).total_seconds() / 60

        # only focus on the most closest one greater than zero
        if difference > 0:
            next_prayer_time_mins = int(difference)
            next_prayer_time_name = prayer_indexes[index]
            break

        recent_difference = 0 - difference
        index += 1

    if not b_is_pressed:
        try:
            upcoming_prayer_time = prayer_times_raw[next_prayer_time_name]
        except KeyError:
            upcoming_prayer_time = 0
            already_prayed = True


    # take the length of the prayer time
    prayer_length = recent_difference + next_prayer_time_mins

    if 0 <= recent_difference <= 2:
        already_prayed = False

    # convert to a percentage and display on bar graph
    percent_remaining = int(round(100 * (next_prayer_time_mins / prayer_length)))

    if next_prayer_time_name not in ["Fajr", "Dhuhr"] and not already_prayed:
        display_snake_pct(percent_remaining, False)

    t = datetime.utcnow()
    sleep_time = 60 - t.second
    for i in range(sleep_time * 20):
        saved_hide_time = hide_time
        saved_already_prayed = already_prayed
        saved_a = a_is_pressed
        saved_b = b_is_pressed
        time.sleep(0.05)
        if saved_hide_time != hide_time or saved_already_prayed != already_prayed\
                or saved_a != a_is_pressed or saved_b != b_is_pressed:
            break
