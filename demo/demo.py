"""Demo pygame game using Sappho.

A very horrible and basic pygame game which
utilizes Sappho (hopefully) to the fullest and
acts as a test.

This could also serve as a template in the future.

Needs to use sprite groups.

"""
 
import pygame

from sappho.collisionsprite import CollisionSprite
from sappho.animatedsprite import AnimatedSprite
from sappho.tilemap import TileMap, Tilesheet, tmx_file_to_tilemaps
from sappho.layers import SurfaceLayers
from sappho.camera import Camera, CameraCenterBehavior

# Constants/game config

# Window resolution in pixels (Width, Height)
RESOLUTION = [700, 500]

# The title that will appear in the window's title bar 
WINDOW_TITLE = "Sappho Engine Test"

# The path to the file that's being used to represent the player
ANIMATED_SPRITE_PATH = "test.gif"

# The path to the file being used as the tilesheet
TILESHEET_PATH = "test_scene/tilesheet.png"

# The Tiled Map Editor file which the player explores
TMX_PATH = "test_scene/test.tmx"

# The layer that the player's sprite will be rendered on 
ANIMATED_SPRITE_Z_INDEX = 0


# Runtime/Main

# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
screen = pygame.display.set_mode(RESOLUTION)
 
# Set the caption in the title bar
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

# The sprite which the player controls
animated_sprite = AnimatedSprite.from_gif(ANIMATED_SPRITE_PATH, mask_threshold=127)
animated_collisionsprite = CollisionSprite(animated_sprite)

# Load the scene, namely the layered map. Layered maps are
# represented as a list of TileMap objects.
tilesheet = Tilesheet.from_file(TILESHEET_PATH, 10, 10)
layer_tilemaps = tmx_file_to_tilemaps(TMX_PATH, tilesheet)

# ... Make a list of surfaces from the tilemaps.
tilemap_surfaces = []

for layer_tilemap in layer_tilemaps:
    tilemap_surfaces.append(layer_tilemap.to_surface())

# Set up the camera
surface_size = (tilemap_surfaces[0].get_width(),
                tilemap_surfaces[0].get_height())

camera = Camera(surface_size, RESOLUTION, (80, 80),
                behavior=CameraCenterBehavior())

# The render layers which we draw to
layers = SurfaceLayers(camera.source_surface, len(tilemap_surfaces))

# Build a list of collidable tiles by layer index.
collidable_tiles_by_layer = {}

for layer_index, layer_tilemap in enumerate(layer_tilemaps):
    solid_tiles = layer_tilemap.set_solid_toplefts()
    solid_tiles_group = pygame.sprite.Group(*solid_tiles)
    collidable_tiles_by_layer[layer_index] = solid_tiles_group

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
    potential_x_coord = x_coord + x_speed
    potential_y_coord = y_coord + y_speed

    potential_rect = pygame.rect.Rect((potential_x_coord, potential_y_coord),
                                      animated_collisionsprite.rect.size)

    solid_tiles_on_players_index = collidable_tiles_by_layer[ANIMATED_SPRITE_Z_INDEX]
    print([t.rect.topleft for t in solid_tiles_on_players_index])

    # NOTE: portion of this could be a collisionsprite method probably...
    # Only move the player if its rect and mask do not
    # collide with tiles.
    colliding = False
    colliding_based_on_rect = pygame.sprite.spritecollide(animated_collisionsprite,
                                                          solid_tiles_on_players_index,
                                                          False,
                                                          collided=pygame.sprite.collide_rect)

    for tile_which_may_be_colliding in colliding_based_on_rect:

        if pygame.sprite.collide_mask(tile_which_may_be_colliding, animated_collisionsprite) is not None:
            colliding = True
            break

    if colliding:
        print("colliding!")
    else:
        y_coord = potential_y_coord
        x_coord = potential_x_coord
        camera.scroll_to(potential_rect)
        animated_collisionsprite.rect.topleft = (x_coord, y_coord)
 
    # DRAWING/RENDER CODE

    # first let's render each tilemap on its respective surface
    for i, tilemap_layer in enumerate(tilemap_surfaces):
        layers[i].blit(tilemap_layer, (0, 0))

    # Finally let's render the animated sprite on some
    # arbitrary layer. In the future the TMX will set this.
    layers[ANIMATED_SPRITE_Z_INDEX].blit(animated_sprite.image, (x_coord, y_coord))
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
