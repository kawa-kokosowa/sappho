#!/usr/bin/env python2

"""Annotate a tilesheet with each tile's IDs, optionally drawing a
border around each tile.

Usage:
    annotatetilesheet.py <input> <tile_width> <tile_height> [options]

Options:
    -o FILE, --output=FILE
        Output to the given FILE instead of "inputfile.annotated.png"
    --border=COLOR
        Enables tile borders and draws them in the given COLOR.
    --font=FONT
        Font to render the tile IDs in. [default: monospace]
    --fontsize=SIZE
        Font size to render the tile IDs in. [default: 24]
    --textcolor=COLOR
        Color of the tile ID text. [default: #000000]
    --scale=SCALE_FACTOR
        Scale factor to resize the tilesheet to before annotating the
        tiles [default: 1]
"""

__version__ = "0.1.0"

import os
import docopt
import pygame

if __name__ == "__main__":
    args = docopt.docopt(__doc__, version=__version__)

    pygame.init()

    # Load the tilesheet
    source = pygame.image.load(args["<input>"])

    # Scale up
    target_size = [a * int(args["--scale"]) for a in source.get_size()]
    tilesheet = pygame.transform.scale(source, target_size)

    tile_size = (int(args["<tile_width>"]) * int(args["--scale"]),
                 int(args["<tile_height>"]) * int(args["--scale"]))

    num_tiles_x = target_size[0] // tile_size[0]
    num_tiles_y = target_size[1] // tile_size[1]

    # Set border color if border drawing is enabled 
    border_color = None
    if args["--border"] is not None:
        border_color = pygame.Color(args["--border"])

    font = pygame.font.SysFont(args["--font"], int(args["--fontsize"]))
    font_color = pygame.Color(args["--textcolor"])

    index = 0
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            xpos = tile_size[0] * x
            ypos = tile_size[1] * y

            rect = pygame.Rect((xpos, ypos), tile_size)
            subsurface = tilesheet.subsurface(rect)

            # Draw borders if enabled
            if border_color is not None:
                pygame.draw.rect(subsurface, border_color,
                                 pygame.Rect((0, 0), tile_size), 1)

            # Draw index
            text = font.render(str(index), True, font_color)
            text_xpos = (tile_size[0] / 2) - (text.get_width() / 2)
            text_ypos = (tile_size[1] / 2) - (text.get_height() / 2)

            subsurface.blit(text, (text_xpos, text_ypos))

            index += 1

    # Check if we've been given an output file, and construct the new
    # filename if we haven't
    filename = args["--output"]
    if not filename:
        name, ext = os.path.splitext(args["<input>"])
        filename = name + ".annotated" + ext

    # Save the image
    pygame.image.save(tilesheet, filename)

    pygame.quit()
