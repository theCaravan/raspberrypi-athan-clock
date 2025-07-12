"""Determine whether Unicorn Hat Mini calls should run in prod or mocked locally"""
import time
import platform

IS_PRODUCTION = platform.system() == "Linux"


if IS_PRODUCTION:
    import unicornhatmini as real_hat
    from gpiozero import Button

    sleep = time.sleep

    # You can expose the real_hat functions directly:
    set_brightness = real_hat.set_brightness
    clear = real_hat.clear
    show = real_hat.show
    set_pixel = real_hat.set_pixel

    BUTTON_B = Button(6)
    BUTTON_A = Button(5)
    BUTTON_Y = Button(24)
    BUTTON_X = Button(16)


else:
    # Mock implementation for Windows (or other dev platforms)
    from mock_hat_mini.index import MockHatMini
    from mock_hat_mini.index import MockButton

    _mock_instance = MockHatMini()

    _sleep_queue = []


    def sleep(seconds) -> None:
        """Non-blocking replacement for time.sleep in GUI mock"""

        def resume() -> None:
            """Resume after sleeping"""
            if _sleep_queue:
                func = _sleep_queue.pop(0)
                func()

        delay_ms = int(seconds * 1000)
        mock_gui.after(delay_ms, resume)
        raise StopIteration


    def set_brightness(value) -> None:
        """Mock Brightness"""
        _mock_instance.set_brightness(value)


    def clear() -> None:
        """Mock Clear"""
        _mock_instance.clear()


    def show() -> None:
        """Mock Show"""
        _mock_instance.show()


    def set_pixel(x, y, r, g, b) -> None:
        """Mock Set Pixel"""
        _mock_instance.set_pixel(x, y, r, g, b)


    mock_gui = _mock_instance

    BUTTON_B = MockButton(6)
    BUTTON_A = MockButton(5)
    BUTTON_Y = MockButton(24)
    BUTTON_X = MockButton(16)
