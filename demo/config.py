"""Configuration constants for Sappho demo."""
import pkg_resources

# Constants/game config

# The path to the file that's being used to represent the player
ANIMATED_SPRITE_PATH = pkg_resources.resource_filename("test_scene", "test.gif")

# The path to the file being used as the tilesheet
TILESHEET_PATH = pkg_resources.resource_filename("test_scene", "tilesheet.png")

# The Tiled Map Editor file which the player explores
TMX_PATH = pkg_resources.resource_filename("test_scene", "test.tmx")

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
