"""Define the constants used in this project"""
from gpiozero import Button

# Set the GPS coordinates for your location
# (Latitude, Longitude, Calculation Method)
#
LOCATION = (45.031553, -93.024759, 2)

# Al Athan API
API_INITIAL_LINK = "https://api.aladhan.com/v1/timings"

# Delay between transitions
TIME_DELAY = 0.05

COLORS = {
    "white":    (255, 255, 255),
    "aqua":     (0, 255, 255),
    "lime":     (0, 255, 0),
    "yellow":   (255, 255, 0),
    "orange":   (255, 165, 0),
    "red":      (255, 0, 0),
    "fuchsia":  (255, 0, 255),
}

PRAYER_INDEXES = {
    0: "Fajr",
    1: "Sunrise",
    2: "Dhuhr",
    3: "Asr",
    4: "Maghrib",
    5: "Isha"
}

# Unicorn Hat Mini Button Mappings
#
# On the Unicorn Hat Mini, the orientation of the buttons are as follows
#
#  B       A
# ._________.
# |         |
# |         |
# |         |
# |         |
# |_________|
#  Y       X

BUTTON_X = Button(16)
BUTTON_Y = Button(24)
BUTTON_B = Button(6)
BUTTON_A = Button(5)

# Unicorn Hat Mini General Configuration
SCREEN_BRIGHTNESS = 0.1

# Numbers to Draw
# This is aligned to the top and left
# The coordinates are ordered in a way that emulates the way a human would draw the number
NUMBERS_TO_DRAW = {
    0: (
        (0, 6),  # * * *
        (0, 5),  # *   *
        (0, 4),  # *   *
        (1, 4),  # *   *
        (2, 4),  # * * *
        (3, 4),
        (4, 4),
        (4, 5),
        (4, 6),
        (3, 6),
        (2, 6),
        (1, 6),
    ),

    1: (
        (1, 6),  #   *
        (0, 5),  # * *
        (1, 5),  #   *
        (2, 5),  #   *
        (3, 5),  # * * *
        (4, 5),
        (4, 6),
        (4, 4),
    ),

    2: (
        (0, 6),  # * * *
        (0, 5),  #     *
        (0, 4),  # * * *
        (1, 4),  # *
        (2, 4),  # * * *
        (2, 5),
        (2, 6),
        (3, 6),
        (4, 6),
        (4, 5),
        (4, 4),
    ),

    3: (
        (0, 6),  # * * *
        (0, 5),  #     *
        (0, 4),  # * * *
        (1, 4),  #     *
        (2, 4),  # * * *
        (2, 5),
        (2, 6),
        (3, 4),
        (4, 4),
        (4, 5),
        (4, 6),
    ),

    4: (
        (0, 6),  # *   *
        (1, 6),  # *   *
        (2, 6),  # * * *
        (2, 5),  #     *
        (0, 4),  #     *
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),
    ),

    5: (
        (0, 4),  # * * *
        (0, 5),  # *
        (0, 6),  # * * *
        (1, 6),  #     *
        (2, 6),  # * * *
        (2, 5),
        (2, 4),
        (3, 4),
        (4, 4),
        (4, 5),
        (4, 6),
    ),

    6: (
        (0, 4),  # * * *
        (0, 5),  # *
        (0, 6),  # * * *
        (1, 6),  # *   *
        (2, 6),  # * * *
        (3, 6),
        (4, 6),
        (4, 5),
        (4, 4),
        (3, 4),
        (2, 4),
        (2, 5),
    ),

    7: (
        (0, 6),  # * * *
        (0, 5),  #     *
        (0, 4),  #     *
        (1, 4),  #     *
        (2, 4),  #     *
        (3, 4),
        (4, 4),
    ),

    8: (
        (1, 6),  # * * *
        (0, 6),  # *   *
        (0, 5),  # * * *
        (0, 4),  # *   *
        (1, 4),  # * * *
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 6),
        (4, 6),
        (4, 5),
        (4, 4),
        (3, 4),
    ),

    9: (
        (2, 5),  # * * *
        (2, 6),  # *   *
        (1, 6),  # * * *
        (0, 6),  #     *
        (0, 5),  # * * *
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),
        (4, 5),
        (4, 6),
    )
}

# Athan Snake
SNAKE_COORDINATES = {
    100:    ((12, 6), COLORS["white"]),
    97:     ((13, 6), COLORS["white"]),
    94:     ((14, 6), COLORS["white"]),
    91:     ((15, 6), COLORS["white"]),
    89:     ((16, 6), COLORS["white"]),
    86:     ((12, 5), COLORS["aqua"]),
    83:     ((13, 5), COLORS["aqua"]),
    80:     ((14, 5), COLORS["aqua"]),
    77:     ((15, 5), COLORS["aqua"]),
    74:     ((16, 5), COLORS["aqua"]),
    71:     ((12, 4), COLORS["lime"]),
    69:     ((13, 4), COLORS["lime"]),
    66:     ((14, 4), COLORS["lime"]),
    63:     ((15, 4), COLORS["lime"]),
    60:     ((16, 4), COLORS["lime"]),
    57:     ((12, 3), COLORS["yellow"]),
    54:     ((13, 3), COLORS["yellow"]),
    51:     ((14, 3), COLORS["yellow"]),
    49:     ((15, 3), COLORS["yellow"]),
    46:     ((16, 3), COLORS["yellow"]),
    43:     ((12, 2), COLORS["orange"]),
    40:     ((13, 2), COLORS["orange"]),
    37:     ((14, 2), COLORS["orange"]),
    34:     ((15, 2), COLORS["orange"]),
    31:     ((16, 2), COLORS["orange"]),
    29:     ((12, 1), COLORS["red"]),
    26:     ((13, 1), COLORS["red"]),
    23:     ((14, 1), COLORS["red"]),
    20:     ((15, 1), COLORS["red"]),
    17:     ((16, 1), COLORS["red"]),
    14:     ((12, 0), COLORS["fuchsia"]),
    11:     ((13, 0), COLORS["fuchsia"]),
    9:      ((14, 0), COLORS["fuchsia"]),
    6:      ((15, 0), COLORS["fuchsia"]),
    3:      ((16, 0), COLORS["fuchsia"])
}
