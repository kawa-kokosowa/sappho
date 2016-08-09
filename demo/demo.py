"""Demo pygame game using Sappho.

A very horrible and basic pygame game which
utilizes Sappho (hopefully) to the fullest and
acts as a test.

This could also serve as a template in the future.

Needs to use sprite groups.

"""
 
import config
import pygame

from sappho.collide import CollisionSprite, Collision
from sappho.animate import AnimatedSprite
from sappho.tiles import TileMap, Tilesheet, tmx_file_to_tilemaps
from sappho.layers import SurfaceLayers
from sappho.camera import Camera, CameraCenterBehavior


# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
screen = pygame.display.set_mode(config.RESOLUTION)
 
# Set the caption in the title bar
pygame.display.set_caption(config.WINDOW_TITLE)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)
 
# TODO: make this work as frame-independent
# speed for movement. Right now this starts
# at 0 and is set to higher when keypress...
x_speed = 0
y_speed = 0

# The sprite which the player controls
animated_sprite = AnimatedSprite.from_gif(config.ANIMATED_SPRITE_PATH, mask_threshold=127)
animated_collisionsprite = CollisionSprite(animated_sprite)
animated_collisionsprite.topleft = config.START_POSITION

# Load the scene, namely the layered map. Layered maps are
# represented as a list of TileMap objects.
tilesheet = Tilesheet.from_file(config.TILESHEET_PATH, *config.START_POSITION)
tilemaps_by_layer = tmx_file_to_tilemaps(config.TMX_PATH, tilesheet)

# ... Make a list of surfaces from the tilemaps.
tilemap_surfaces = []

for tilemap_representing_layer in tilemaps_by_layer:
    tilemap_surfaces.append(tilemap_representing_layer.to_surface())

# Set up the camera
surface_size = tilemap_surfaces[0].get_size()
camera = Camera(surface_size, config.RESOLUTION, (80, 80),
                behavior=CameraCenterBehavior())

# The render layers which we draw to
layers = SurfaceLayers(camera.source_surface, len(tilemap_surfaces))

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
 
    # Test if the player is going to collide with any other objects
    # and if not, move the player

    # Move the object according to the speed vector.
    #
    # We will be resetting animated_collisionsprite.rect.topleft
    # to old_topleft if there is a collision.
    tilemap_on_players_index = tilemaps_by_layer[config.ANIMATED_SPRITE_Z_INDEX]
    collision_group_on_player_index = tilemap_on_players_index.collision_group

    try:
        animated_collisionsprite.try_to_move(x_speed, y_speed, collision_group_on_player_index)
    except Collision:
        pass
    else:
        camera.scroll_to(animated_collisionsprite.rect)
 
    # DRAWING/RENDER CODE

    # first let's render each tilemap on its respective surface
    for i, tilemap_layer in enumerate(tilemap_surfaces):
        layers[i].blit(tilemap_layer, (0, 0))

    # Finally let's render the animated sprite on some
    # arbitrary layer. In the future the TMX will set this.
    layers[config.ANIMATED_SPRITE_Z_INDEX].blit(animated_sprite.image,
                                                animated_collisionsprite.rect.topleft)

    # ... Draw those layers!
    layers.render()
     
    # Let's get the timedelta and then send it to the appropriate things...
    timedelta = clock.get_time()
    camera.update_state("hahahahahah lies lies lies")
    animated_sprite.update_state(timedelta)
 
    # Go ahead and update the screen with what we've drawn.
    screen.blit(camera, (0, 0))
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
