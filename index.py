"""Main Program"""
import datetime

from adjustable_settings import (SCREEN_BRIGHTNESS)
from buttons import setup_hardware_buttons
from functions import (clear_section,
                       display_number, test_numbers)
import mock_hat_mini.bridge as unicornhatmini
import state
from state import current, clock_state


def update_time_vars() -> (any, any, any):
    """Update global time-related variables and handle special modes."""
    datetime_now = datetime.datetime.now()
    current.date = datetime_now.strftime("%d/%m/%Y")

    current.hour = datetime_now.strftime("%H")
    current.minute = datetime_now.strftime("%M")

    return current.hour, current.minute, current.date


def display_clock(clock_hour, clock_minute, year = None) -> None:
    """Draw hours, minutes and optionally year on display."""
    if int(clock_minute) == 0 or state.initial_run:
        clear_section(0, 4, 0, 6)

        if len(clock_hour) == 2:
            display_number(int(clock_hour[0]), 0, 0)
            display_number(int(clock_hour[1]), 0, -4)
        else:
            display_number(int(clock_hour), 0, -2)

        state.initial_run = False

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


def main_clock_loop() -> None:
    """Main update loop called repeatedly."""
    main_hour, main_minute, today_date_str = update_time_vars()

    if clock_state.hide_clock:
        pass
    else:
        display_clock(main_hour, main_minute)

    utc_tz = datetime.timezone.utc
    now = datetime.datetime.now(utc_tz)
    seconds_until_next_minute = 60 - now.second - now.microsecond / 1_000_000

    unicornhatmini.sleep(seconds_until_next_minute, continuation = main_clock_loop)


def main() -> None:
    """Main"""
    setup_hardware_buttons()
    unicornhatmini.set_brightness(SCREEN_BRIGHTNESS)
    test_numbers()
    main_clock_loop()


if __name__ == "__main__":
    if hasattr(unicornhatmini, "mock_gui"):
        main()
        unicornhatmini.mock_gui.mainloop()
    else:
        main()
