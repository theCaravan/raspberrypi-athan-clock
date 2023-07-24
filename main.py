"""Main Program"""
from functions import *

unicornhatmini.set_brightness(SCREEN_BRIGHTNESS)

# Run a display of all the numbers as a welcome greeting and a diagnostic
test_numbers()

# Set none of the buttons as pressed
b_is_pressed_next_prayer = False
a_is_pressed_hijri_date = False
y_is_pressed_already_prayed = False
x_is_pressed_hide_time = False

initial_run = True
error_in_athan = False

prayer_times_raw = {}
prayer_times_date = ""
upcoming_prayer_time = ""
hijri_date_raw = ""


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
    year = ""
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
        year = hijri_date_raw.split("/")[2]

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

    if year:
        display_number(int(year[0]), -5, 0)
        display_number(int(year[1]), -5, -4)

    # Only grab this if we didn't have them stored or if it's the wrong day
    if not error_in_athan and (prayer_times_raw == {} or prayer_times_date == "" or prayer_times_date != today_date_str):
        raw_request = get_prayer_times(current_unix_time, LOCATION_LATITUDE_, LOCATION_LONGITUDE, LOCATION_CALC_MTHD)

        if raw_request["result"] == "error":
            error_in_athan = True

        else:
            prayer_times_raw = raw_request["r.text"]["data"]["timings"]
            hijri_date_raw = "{}/{}/{}".format(raw_request["data"]["date"]["hijri"]["month"]["number"],
                                               raw_request["data"]["date"]["hijri"]["day"],
                                               raw_request["data"]["date"]["hijri"]["year"][2:])

    if error_in_athan:
        display_snake_error()

    else:
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

        # Always show entire snake on next prayer time
        if b_is_pressed_next_prayer:
            percent_remaining = 100

        if next_prayer_time_name not in ["Fajr", "Dhuhr"] \
                and not y_is_pressed_already_prayed\
                and percent_remaining != 0:
            display_snake_pct(percent_remaining)

    just_pressed = False
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
            just_pressed = True
            break

    # Clear new screen pressed buttons if this wasn't just pressed
    # Allows a screen to reset to the main on its own at the next minute
    if not just_pressed:
        a_is_pressed_hijri_date = False
        b_is_pressed_next_prayer = False
        unicornhatmini.clear()
        initial_run = True
