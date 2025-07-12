"""Main Program"""
from datetime import datetime
import time

from adjustable_settings import (LOCATION_LATITUDE_,
                                 LOCATION_LONGITUDE,
                                 LOCATION_CALC_MTHD,
                                 TIME_DELAY, SCREEN_BRIGHTNESS)
from constants import PRAYER_INDEXES
from functions import (display_snake_pct,
                       test_numbers,
                       display_number,
                       clear_section,
                       get_prayer_times, display_snake_error)
import mock_hat_mini.bridge as unicornhatmini

initial_run = True
a_is_pressed_hijri_date = False
b_is_pressed_next_prayer = False
y_is_pressed_already_prayed = False
x_is_pressed_hide_time = False

hour = 0
minute = 0
prayer_times_raw = {}
prayer_times_date = ""
error_in_athan = ""
upcoming_prayer_time = ""
hijri_date_raw = ""


def pressed_b_next_prayer() -> None:
    """Show the next prayer time (or back to clock) when pressing the B (upper left) button on
    the Unicorn Hat Mini"""
    global b_is_pressed_next_prayer
    global initial_run

    if b_is_pressed_next_prayer:
        b_is_pressed_next_prayer = False
        unicornhatmini.clear()
        unicornhatmini.show()
        initial_run = True

    else:
        b_is_pressed_next_prayer = True


def pressed_a_hijri_date() -> None:
    """Show the Hijri date (or back to clock) when pressing the A (upper right) button on the
    Unicorn Hat Mini"""
    global a_is_pressed_hijri_date
    global initial_run

    if a_is_pressed_hijri_date:
        a_is_pressed_hijri_date = False
        unicornhatmini.clear()
        unicornhatmini.show()
        initial_run = True
    else:
        a_is_pressed_hijri_date = True


def pressed_y_already_prayed() -> None:
    """Hide/Show the Athan Snake when pressing the Y (bottom left) button on the Unicorn Hat Mini"""
    global y_is_pressed_already_prayed

    if y_is_pressed_already_prayed:
        y_is_pressed_already_prayed = False
    else:
        y_is_pressed_already_prayed = True


def pressed_x_hide_time() -> None:
    """Hide/Show the clock when pressing the X (bottom right) button on the Unicorn Hat Mini"""
    global x_is_pressed_hide_time

    if x_is_pressed_hide_time:
        x_is_pressed_hide_time = False
    else:
        x_is_pressed_hide_time = True


def setup_buttons() -> None:
    """Assign button press handlers."""
    unicornhatmini.BUTTON_B.when_pressed = pressed_b_next_prayer
    unicornhatmini.BUTTON_A.when_pressed = pressed_a_hijri_date
    unicornhatmini.BUTTON_Y.when_pressed = pressed_y_already_prayed
    unicornhatmini.BUTTON_X.when_pressed = pressed_x_hide_time


def update_time_vars() -> (any, any, any):
    """Update global time-related variables and handle special modes."""
    global hour, minute, initial_run, b_is_pressed_next_prayer, a_is_pressed_hijri_date, \
        x_is_pressed_hide_time
    global hijri_date_raw, upcoming_prayer_time

    datetime_now = datetime.now()
    today_date_str = datetime_now.strftime("%d/%m/%Y")

    if x_is_pressed_hide_time:
        # Hide time mode
        a_is_pressed_hijri_date = False
        b_is_pressed_next_prayer = False
        initial_run = True
        unicornhatmini.clear()
        return None, None, today_date_str

    if b_is_pressed_next_prayer:
        a_is_pressed_hijri_date = False
        x_is_pressed_hide_time = False
        initial_run = True
        unicornhatmini.clear()
        if upcoming_prayer_time:
            hour, minute = upcoming_prayer_time.split(":")
        else:
            # fallback to clock
            return None, None, today_date_str

    elif a_is_pressed_hijri_date:
        b_is_pressed_next_prayer = False
        x_is_pressed_hide_time = False
        initial_run = True
        unicornhatmini.clear()
        hour, minute, *_ = hijri_date_raw.split("/")

    else:
        hour = datetime_now.strftime("%H")
        minute = datetime_now.strftime("%M")

    return hour, minute, today_date_str


def display_clock(clock_hour, clock_minute, year = None) -> None:
    """Draw hours, minutes and optionally year on display."""
    global initial_run

    if int(clock_minute) == 0 or initial_run:
        clear_section(0, 4, 0, 6)

        if len(clock_hour) == 2:
            display_number(int(clock_hour[0]), 0, 0)
            display_number(int(clock_hour[1]), 0, -4)
        else:
            display_number(int(clock_hour), 0, -2)

        initial_run = False

    if int(clock_minute) in [0, 10, 20, 30, 40, 50]:
        clear_section(6, 10, 0, 6)
    else:
        clear_section(6, 10, 0, 2)

    if len(clock_minute) == 2:
        display_number(int(clock_minute[0]), 6, 0)
        display_number(int(clock_minute[1]), 6, -4)
    else:
        display_number(0, 6, 0)
        display_number(int(clock_minute), 6, -4)

    if year:
        display_number(int(year[0]), -5, 0)
        display_number(int(year[1]), -5, -4)


def update_prayer_times(today_date_str) -> None:
    """Fetch and update prayer times if needed."""
    global prayer_times_raw, prayer_times_date, error_in_athan, hijri_date_raw

    check_a = not error_in_athan
    check_b = prayer_times_raw == {}
    check_c = prayer_times_date == ""
    check_d = prayer_times_date != today_date_str
    if check_a and (check_b or check_c or check_d):
        try:
            current_unix_time = int(time.mktime(datetime.now().timetuple()))
            raw_request = get_prayer_times(current_unix_time,
                                           LOCATION_LATITUDE_,
                                           LOCATION_LONGITUDE,
                                           LOCATION_CALC_MTHD
                                           )

            if raw_request["result"] == "error":
                error_in_athan = True
            else:
                raw_data = raw_request["r.text"]
                prayer_times_raw = raw_data["data"]["timings"]
                hijri_date_raw = "{}/{}/{}".format(
                    raw_data["data"]["date"]["hijri"]["month"]["number"],
                    raw_data["data"]["date"]["hijri"]["day"],
                    raw_data["data"]["date"]["hijri"]["year"][2:]
                    )
                prayer_times_date = today_date_str
        except Exception as e:
            print("error_in_athan", e)
            error_in_athan = True


def display_prayer_snake(snake_hour, snake_minute) -> None:
    """Handle logic to display prayer snake or error."""
    global prayer_times_raw, y_is_pressed_already_prayed, upcoming_prayer_time

    if error_in_athan:
        display_snake_error()
        return

    prayer_times = []
    for prayer_time in prayer_times_raw.keys():
        if prayer_time in ["Sunset", "Imsak", "Midnight", "Firstthird", "Lastthird"]:
            continue
        prayer_times.append(datetime.strptime(f"{prayer_times_date} "
                                              f"{prayer_times_raw[prayer_time]}",
                                              "%d/%m/%Y %H:%M"
                                              )
                            )

    right_now = datetime.strptime(f"{prayer_times_date} {snake_hour}:{snake_minute}",
                                  "%d/%m/%Y %H:%M"
                                  )

    next_prayer_time_name = ""
    next_prayer_time_minutes = 0
    recent_difference = 0
    index = 0

    for prayer_time in prayer_times:
        difference = (prayer_time - right_now).total_seconds() / 60
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

    prayer_length = recent_difference + next_prayer_time_minutes

    if 0 <= recent_difference <= 2:
        y_is_pressed_already_prayed = False

    if prayer_length != 0:
        percent_remaining = int(round(100 * (next_prayer_time_minutes / prayer_length)))
    else:
        percent_remaining = 0

    if b_is_pressed_next_prayer:
        percent_remaining = 100

    check_e = next_prayer_time_name not in ["Fajr", "Dhuhr"]
    check_f = not y_is_pressed_already_prayed
    check_g = percent_remaining != 0
    if check_e and check_f and check_g:
        display_snake_pct(percent_remaining)


def reset_button_flags_if_needed(just_pressed) -> None:
    """Reset button flags if no button was just pressed."""
    global a_is_pressed_hijri_date, b_is_pressed_next_prayer, initial_run

    if not just_pressed:
        a_is_pressed_hijri_date = False
        b_is_pressed_next_prayer = False
        unicornhatmini.clear()
        initial_run = True


def wait_for_next_tick(iteration = 0, max_iterations = None) -> None:
    """Non-blocking wait loop using Tkinter after(), checking buttons regularly."""
    global a_is_pressed_hijri_date, b_is_pressed_next_prayer, y_is_pressed_already_prayed, \
        x_is_pressed_hide_time

    saved_b = b_is_pressed_next_prayer
    saved_a = a_is_pressed_hijri_date
    saved_y = y_is_pressed_already_prayed
    saved_x = x_is_pressed_hide_time

    # Check for button changes
    if (saved_b != b_is_pressed_next_prayer or
        saved_a != a_is_pressed_hijri_date or
        saved_y != y_is_pressed_already_prayed or
        saved_x != x_is_pressed_hide_time):
        main_clock_loop()
        return

    # Check if done waiting
    if max_iterations is not None and iteration >= max_iterations:
        main_clock_loop()
        return

    # Schedule next check
    unicornhatmini.mock_gui.after(int(TIME_DELAY * 1000),
                                  lambda: wait_for_next_tick(iteration + 1, max_iterations)
                                  )


def main_clock_loop() -> None:
    """Main update loop called repeatedly."""
    main_hour, main_minute, today_date_str = update_time_vars()
    if main_hour is None or main_minute is None:
        # Possibly hide mode, just skip drawing clock
        pass
    else:
        display_clock(main_hour, main_minute)
        update_prayer_times(today_date_str)
        display_prayer_snake(main_hour, main_minute)

    t = datetime.utcnow()
    sleep_time = 60 - t.second
    max_iterations = sleep_time * int(1 / TIME_DELAY)

    wait_for_next_tick(max_iterations)


def main():
    """Main"""
    setup_buttons()
    unicornhatmini.set_brightness(SCREEN_BRIGHTNESS)
    test_numbers()
    main_clock_loop()


if __name__ == "__main__":
    if hasattr(unicornhatmini, "mock_gui"):
        unicornhatmini.mock_gui.after(100, main)
        unicornhatmini.mock_gui.mainloop()
    else:
        main()
