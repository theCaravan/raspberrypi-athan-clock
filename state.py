"""Keep the global state of these variables, which change over time"""


class IsPressed:
    """Track which button is pressed; pressing one resets the others."""

    def __init__(self) -> None:
        self.a = False
        self.b = False
        self.x = False
        self.y = False

    def press_a(self) -> None:
        """Reset all other buttons than A"""
        self.a = True
        self.b = False
        self.x = False
        self.y = False

    def press_b(self) -> None:
        """Reset all other buttons than B"""
        self.a = False
        self.b = True
        self.x = False
        self.y = False

    def press_x(self) -> None:
        """Reset all other buttons than X"""
        self.a = False
        self.b = False
        self.x = True
        self.y = False

    def press_y(self) -> None:
        """Reset all other buttons than Y"""
        self.a = False
        self.b = False
        self.x = False
        self.y = True

    def reset_all(self) -> None:
        """Reset all buttons to False"""
        self.a = False
        self.b = False
        self.x = False
        self.y = False


class ClockState:
    """Define states of the clock"""

    def __init__(self) -> None:
        self.hide_clock = False


class Current:
    """Define current date time events"""

    def __init__(self, hour: int = 0, minute: int = 0, date: str = "") -> None:
        self.hour = hour
        self.minute = minute
        self.date = date


current = Current()
is_pressed = IsPressed()
clock_state = ClockState()

initial_run = True
prayer_times_raw = {}
prayer_times_date = ""
error_in_athan = ""
upcoming_prayer_time = ""
hijri_date_raw = ""
