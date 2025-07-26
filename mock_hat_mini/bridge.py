"""Determine whether Unicorn Hat Mini calls should run in prod or mocked locally"""
import time
import platform

IS_PRODUCTION = platform.system() == "Linux"

if IS_PRODUCTION:
    import unicornhatmini as real_hat
    from gpiozero import Button


    def sleep(seconds, continuation = None) -> None:
        """Basically, regular sleep, but handle continuation"""
        time.sleep(seconds)
        if continuation:
            continuation()


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


    def tk_sleep(seconds: float, continuation = None) -> None:
        """Mock sleep function in Tk, with optional continuation callback"""
        total_delay = seconds + 0.007  # Extra delay to simulate hardware timing
        milliseconds = int(total_delay * 1000)

        if continuation is not None:
            # Schedule the continuation to run after the delay without blocking
            _mock_instance.after(milliseconds, continuation)
        else:
            # No continuation: block with event loop until done
            done = [False]

            def mark_done() -> None:
                """Mark done"""
                done[0] = True

            _mock_instance.after(milliseconds, mark_done)

            while not done[0]:
                _mock_instance.update()


    sleep = tk_sleep


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
