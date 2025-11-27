"""Handle button presses"""
import threading

import state
import mock_hat_mini.bridge as unicornhatmini


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


# Callback that will be set by index.py
_update_display_callback = None


def set_update_display_callback(callback: object) -> None:
    """Set the callback to trigger immediate display updates"""
    global _update_display_callback
    _update_display_callback = callback


# Create and export the singleton instance
buttons = Buttons()


def handle_a_pressed() -> None:
    """Handle button A press - toggle hijri date"""
    print("Button A pressed — toggle hijri date")

    state.is_pressed.a = not state.is_pressed.a
    state.clock_state.display_mode = (
        state.DisplayMode.HIJRI if state.is_pressed.a else state.DisplayMode.CLOCK
    )
    unicornhatmini.clear()
    unicornhatmini.show()
    state.initial_run = True


def handle_b_pressed() -> None:
    """Handle button B press - toggle next prayer"""
    print("Button B pressed — toggle next prayer")

    state.is_pressed.b = not state.is_pressed.b
    state.clock_state.display_mode = (
        state.DisplayMode.PRAYER if state.is_pressed.b else state.DisplayMode.CLOCK
    )
    unicornhatmini.clear()
    unicornhatmini.show()
    state.initial_run = True


def handle_x_pressed() -> None:
    """Handle button X press - toggle hide clock (blank screen)"""
    state.is_pressed.x = not state.is_pressed.x
    state.clock_state.hide_clock = state.is_pressed.x
    print(f"Button X pressed — {'hiding' if state.is_pressed.x else 'showing'} clock")

    unicornhatmini.clear()
    unicornhatmini.show()
    state.initial_run = True


def handle_y_pressed() -> None:
    """Handle button Y press - toggle already prayed"""
    state.is_pressed.y = not state.is_pressed.y
    print(f"Button Y pressed — already prayed: {state.is_pressed.y}")


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
