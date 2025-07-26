"""Mock the Unicorn Hat Mini in a GUI via Tkinter"""
import tkinter as tk

# Configuration
ORIENTATION = 1  # 0=Horizontal, 1=Vertical (rotated left 90°)

# Original grid size
ROWS = 17
COLS = 7

# Adjusted sizes based on orientation
if ORIENTATION == 1:
    DISPLAY_ROWS, DISPLAY_COLS = ROWS, COLS  # Horizontal: 16 rows, 7 cols
else:
    DISPLAY_ROWS, DISPLAY_COLS = COLS, ROWS  # Vertical: 7 rows, 16 cols

CELL_SIZE = 12
BUTTON_SIZE = int(CELL_SIZE * 1.5)


class MockHatMini(tk.Tk):
    """Mocks a Unicorn Hat Mini (17 x 7)"""

    def __init__(self) -> None:
        super().__init__()
        self.title("LED Simulator with Orientation")

        total_width = DISPLAY_COLS * CELL_SIZE
        total_height = DISPLAY_ROWS * CELL_SIZE + 2 * (BUTTON_SIZE + 10)
        self.geometry(f"{total_width}x{total_height}")
        self.resizable(False, False)
        self.center_window(total_width, total_height)

        self.main_frame = tk.Frame(self, bg = "black")
        self.main_frame.pack()

        self.create_button_row()
        self.canvas = tk.Canvas(
            self.main_frame,
            width = DISPLAY_COLS * CELL_SIZE,
            height = DISPLAY_ROWS * CELL_SIZE,
            bg = 'black',
            highlightthickness = 0
            )
        self.canvas.pack()
        self.create_button_row(top = False)
        self._button_handlers = {}

        self.leds = []
        self.draw_grid()

    def center_window(self, width, height) -> None:
        """Center window"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def draw_grid(self) -> None:
        """Draw grid"""
        self.leds.clear()
        for row in range(DISPLAY_ROWS):
            row_leds = []
            for col in range(DISPLAY_COLS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                led = self.canvas.create_oval(
                    x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                    fill = 'gray20', outline = 'gray40'
                    )
                row_leds.append(led)
            self.leds.append(row_leds)

    def set_led(self, row, col, color) -> None:
        """Set LED"""
        if 0 <= row < DISPLAY_ROWS and 0 <= col < DISPLAY_COLS:
            self.canvas.itemconfig(self.leds[row][col], fill = color)

    @staticmethod
    def _map_coordinates(x, y) -> (int, int):
        if ORIENTATION == 0:
            # horizontal, no change
            return y, x  # row, col
        else:
            # vertical = rotate left 90 deg:
            # new_row = x
            # new_col = (ROWS - 1) - y  (flip)
            return x, (DISPLAY_COLS - 1) - y

    def set_pixel(self, x, y, r, g, b) -> None:
        """Set pixel"""
        color = f'#{r:02x}{g:02x}{b:02x}'
        row, col = self._map_coordinates(x, y)
        self.set_led(row, col, color)

    def clear(self) -> None:
        """Clear display"""
        for row in range(DISPLAY_ROWS):
            for col in range(DISPLAY_COLS):
                self.set_led(row, col, 'black')

    def show(self) -> None:
        """Show display, though it does nothing here as its instant"""
        pass

    def set_brightness(self, value) -> None:
        """Set brightness, but not needed here"""
        pass

    def create_button_row(self, top = True) -> None:
        """Create button row"""
        frame = tk.Frame(self.main_frame, bg = "black")
        frame.pack(pady = 4)

        # Decide labels & positions based on orientation & top/bottom
        if ORIENTATION == 0:
            if top:
                left_label, right_label = "B", "A"
            else:
                left_label, right_label = "Y", "X"
        else:
            # Vertical orientation (rotated left)
            if top:
                left_label, right_label = "A", "X"
            else:
                left_label, right_label = "B", "Y"

        # Left button
        self._create_button_with_label(
            frame, left_label,
            text_side = "left",
            justify = "right"
            )

        spacer_width = (DISPLAY_COLS * CELL_SIZE) - (2 * BUTTON_SIZE) - 40
        spacer = tk.Frame(frame, width = spacer_width, bg = "black")
        spacer.pack(side = "left")

        # Right button
        self._create_button_with_label(
            frame, right_label,
            text_side = "right",
            justify = "left"
            )

    def _create_button_with_label(self, parent, button_label, text_side, justify) -> None:
        container = tk.Frame(parent, bg = "black")
        container.pack(side = "left")

        if text_side == "left":
            tk.Label(container, text = button_label, fg = "white", bg = "black",
                     font = ("Arial", int(BUTTON_SIZE * 0.4)), justify = justify
                     ).pack(side = "left", padx = (0, 5))

        canvas = tk.Canvas(container, width = BUTTON_SIZE, height = BUTTON_SIZE,
                           bg = "black", highlightthickness = 0
                           )
        canvas.pack(side = "left")

        circle = canvas.create_oval(2, 2, BUTTON_SIZE - 2, BUTTON_SIZE - 2,
                                    fill = "white", outline = "gray40"
                                    )

        canvas.tag_bind(circle,
                        "<Button-1>",
                        lambda e, _ = button_label: self.handle_button_press(_)
                        )

        if text_side == "right":
            tk.Label(container, text = button_label, fg = "white", bg = "black",
                     font = ("Arial", int(BUTTON_SIZE * 0.4)), justify = justify
                     ).pack(side = "left", padx = (5, 0))

    def set_button_handlers(self, a = None, b = None, y = None, x = None) -> None:
        """Set button handlers"""
        self._button_handlers = {'A': a, 'B': b, 'Y': y, 'X': x}

    def handle_button_press(self, label) -> None:
        """Handle button press"""
        handler = self._button_handlers.get(label)
        if handler:
            handler()
        else:
            print(f"Button {label} pressed, no handler registered.")

    def test_pattern(self) -> None:
        import colorsys
        for i in range(min(ROWS, COLS)):
            hue = i / float(min(ROWS, COLS))
            r, g, b = [int(255 * x) for x in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
            self.set_pixel(i, i, r, g, b)


class MockButton:
    """Mock Button on Tk"""

    def __init__(self, pin, master = None, **kwargs) -> None:
        self.pin = pin
        self._when_pressed = None

        # Create a Tkinter Button widget (visible or hidden)
        self.button = tk.Button(master, text = f"Button {pin}", **kwargs)
        self.button.pack(padx = 5, pady = 5)

        # Bind Tk button click to internal handler
        self.button.bind("<Button-1>", self._on_button_click)

    def _on_button_click(self, _) -> None:
        if callable(self._when_pressed):
            self._when_pressed()

    @property
    def when_pressed(self) -> any:
        """When pressed"""
        return self._when_pressed

    @when_pressed.setter
    def when_pressed(self, callback) -> None:
        self._when_pressed = callback
