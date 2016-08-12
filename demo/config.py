# Constants/game config

MAX_SPEED = 2

RESOLUTION = [700, 500]
"""tuple(int, int): This demo will be ran in a window of the
dimensions (x, y) pixels (width, height).
"""

VIEWPORT = (80, 80)
"""tuple(int, int): ..."""

WINDOW_TITLE = "Sappho Engine Test"
"""str: The title of the window running the demo.

The text which appears in the titlebar of the window.
"""

ANIMATED_SPRITE_PATH = "test.gif"
"""str: path to animated GIF to use as player's sprite."""

TILESHEET_PATH = "test_scene/tilesheet.png"
"""str: path to file to be used as the tilesheet for
drawing the map.

I've only tested PNGs.
"""

TMX_PATH = "test_scene/test.tmx"
"""str: path to Tiled Map Editor file, this will be used
to draw our level, which the player will explore.
"""

ANIMATED_SPRITE_Z_INDEX = 0
"""int: The layer the player's sprite will be rendered on.

0 is farthest back, and higher numbers increase toward the
foreground. The number of layers will correspond with the
map that's being loaded.
"""

START_POSITION = (10, 10)
"""tuple(int, int): The absolute pixel coordinate
of the player's starting position on the map.
"""
