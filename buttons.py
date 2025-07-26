"""Handle button presses"""
import threading

from state import is_pressed


class Buttons:
    """Defines buttons and how to handle them"""

    def __init__(self) -> None:
        self._flag_lock = threading.Lock()
        self._flags = {
            'A': False,
            'B': False,
            'Y': False,
            'X': False,
            }

    def toggle_flag(self, button_key: str) -> None:
        """Toggle button press flag"""
        with self._flag_lock:
            if button_key in self._flags:
                self._flags[button_key] = not self._flags[button_key]

    def get_flag(self, button_key: str) -> bool:
        """Return button press flag"""
        with self._flag_lock:
            return self._flags.get(button_key, False)


# Create and export the singleton instance
buttons = Buttons()


def handle_a_pressed() -> None:
    """Handle button A press"""
    is_pressed.a = not is_pressed.a
    print("Button A pressed — toggle hijri date")


def handle_b_pressed() -> None:
    """Handle button B press"""
    is_pressed.b = not is_pressed.b
    print("Button B pressed — toggle next prayer")


def handle_y_pressed() -> None:
    """Handle button Y press"""
    is_pressed.y = not is_pressed.y
    print("Button Y pressed — toggle already prayed")


def handle_x_pressed() -> None:
    """Handle button X press"""
    is_pressed.x = not is_pressed.x
    print("Button X pressed — toggle hide clock")


def setup_hardware_buttons() -> None:
    """Set up buttons"""
    from mock_hat_mini import bridge

    if hasattr(bridge, "mock_gui"):
        bridge.mock_gui.set_button_handlers(
            a = handle_a_pressed,
            b = handle_b_pressed,
            y = handle_y_pressed,
            x = handle_x_pressed,
            )
    else:
        bridge.BUTTON_A.when_pressed = handle_a_pressed
        bridge.BUTTON_B.when_pressed = handle_b_pressed
        bridge.BUTTON_Y.when_pressed = handle_y_pressed
        bridge.BUTTON_X.when_pressed = handle_x_pressed
