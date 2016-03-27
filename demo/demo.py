"""Demo pygame game using Sappho.

A very horrible and basic pygame game which
utilizes Sappho (hopefully) to the fullest and
acts as a test.

This could also serve as a template in the future.

"""
 
import pygame

from sappho import (AnimatedSprite,
                    TileMap,
                    Tilesheet,
                    tmx_file_to_tilemaps,
                    SurfaceLayers,
                    Camera,
                    CameraCenterBehavior)

# Constants/game config
RESOLUTION = [700, 500]
WINDOW_TITLE = "Sappho Engine Test"
ANIMATED_SPRITE_PATH = "test.gif"
TILESHEET_PATH = "test_scene/tilesheet.png"
TMX_PATH = "test_scene/test.tmx"
ANIMATED_SPRITE_Z_INDEX = 0


# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
screen = pygame.display.set_mode(RESOLUTION)
 
pygame.display.set_caption(WINDOW_TITLE)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)
 
# Speed in pixels per frame
x_speed = 0
y_speed = 0
 
# Current position
x_coord = 10
y_coord = 10

# The player will be able to control this with arrow keys.
animated_sprite = AnimatedSprite.from_file(ANIMATED_SPRITE_PATH)

# Load the scene, namely the layered map. Layered maps are
# represented as a list of TileMap objects.
tilesheet = Tilesheet.from_file(TILESHEET_PATH, 10, 10)
layer_tilemaps = tmx_file_to_tilemaps(TMX_PATH, tilesheet)

# ... Make a list of surfaces from the tilemaps.
tilemap_surfaces = []

for layer_tilemap in layer_tilemaps:
    tilemap_surfaces.append(layer_tilemap.to_surface())

surface_size = (tilemap_surfaces[0].get_width(),
                tilemap_surfaces[0].get_height())

camera = Camera(surface_size, RESOLUTION, (80, 80))
behavior = CameraCenterBehavior(camera)
camera.behavior = behavior

# The render layers which we draw to
layers = SurfaceLayers(camera, len(tilemap_surfaces))
 
# Main program loop
while not done:

    # Process events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
 
        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:

            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3
 
        # User let up on a key
        elif event.type == pygame.KEYUP:

            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0
 
    # GAME LOGIC
 
    # Move the object according to the speed vector.
    potential_x_coord = x_coord + x_speed
    potential_y_coord = y_coord + y_speed

    rect = pygame.rect.Rect((potential_x_coord, potential_y_coord),
                            animated_sprite.image.get_size())

    tilemap_on_players_index = layer_tilemaps[ANIMATED_SPRITE_Z_INDEX]
    solid_blocks_on_players_index = tilemap_on_players_index.solid_blocks

    if rect.collidelist(solid_blocks_on_players_index) != -1:
        print("colliding!")
    else:
        y_coord = potential_y_coord
        x_coord = potential_x_coord

        # XXX
        # Scroll the viewport to where our character is. This could be improved
        # to only scroll when reaching the edges of the viewport, but this
        # works for now.
        camera.scroll_to(rect)
        #camera.scroll_absolute(x_coord - 10, y_coord - 10)
 
    # DRAWING/RENDER CODE

    # first let's render each tilemap on its respective surface
    for i, tilemap_layer in enumerate(tilemap_surfaces):
        layers[i].blit(tilemap_layer, (0, 0))

    # Finally let's render the animated sprite on some
    # arbitrary layer. In the future the TMX will set this.
    layers[ANIMATED_SPRITE_Z_INDEX].blit(animated_sprite.image, (x_coord, y_coord))

    # Draw the layers and update the animations with the time
    layers.render()
    animated_sprite.update(clock)
 
    # Go ahead and update the screen with what we've drawn.
    screen.blit(camera, (0, 0))
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
