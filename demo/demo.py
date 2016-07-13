"""Demo pygame game using Sappho.

A very horrible and basic pygame game which
utilizes Sappho (hopefully) to the fullest and
acts as a test.

This could also serve as a template in the future.

Needs to use sprite groups.

"""
 
import pygame
import time
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)

from sappho.animatedsprite import AnimatedSprite
from sappho.tilemap import TileMap, Tilesheet, tmx_file_to_tilemaps
from sappho.layers import SurfaceLayers
from sappho.camera import Camera, CameraCenterBehavior
from sappho import particle

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
animated_sprite = AnimatedSprite.from_file(ANIMATED_SPRITE_PATH)

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

# Constructing particle system...
fountain = particle.ParticleSystem(
    particle.Particle(40, 10, life=7),
    emitter=particle.EmitterConstantRate(30),
    launcher=particle.PhysicsComposite(
        particle.PhysicsKick(dx=2, dy=-10),
        particle.PhysicsJitter(5, 5, 5, 5, 3),
    ),
    physics=particle.PhysicsComposite(
        particle.PhysicsInertia(),
        particle.PhysicsAcceleration(0, 10),
    ),
    drawer=particle.DrawerSimple(
        pygame.transform.scale(
            pygame.image.load("fuzzball.png"),
            (5, 5),
        ),
        pygame.BLEND_RGB_ADD,
    )
)


last_time = time.time()
# Main program loop
while not done:
    new_time = time.time()
    elapsed = new_time - last_time
    last_time = new_time

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
                            animated_sprite.image.get_size())

    tilemap_on_players_index = layer_tilemaps[ANIMATED_SPRITE_Z_INDEX]
    solid_blocks_on_players_index = tilemap_on_players_index.get_solid_blocks()

    if potential_rect.collidelist(solid_blocks_on_players_index) != -1:
        print("colliding!")
    else:
        y_coord = potential_y_coord
        x_coord = potential_x_coord
        camera.scroll_to(potential_rect)
        #camera.scroll_absolute(x_coord - 10, y_coord - 10)

    fountain.update_state(elapsed)
 
    # DRAWING/RENDER CODE

    # first let's render each tilemap on its respective surface
    for i, tilemap_layer in enumerate(tilemap_surfaces):
        layers[i].blit(tilemap_layer, (0, 0))

    # Finally let's render the animated sprite on some
    # arbitrary layer. In the future the TMX will set this.
    layers[ANIMATED_SPRITE_Z_INDEX].blit(animated_sprite.image, (x_coord, y_coord))

    fountain.draw_on(layers[ANIMATED_SPRITE_Z_INDEX])

    # Draw the layers and update the animations with the time
    layers.render()
    camera.update()
    animated_sprite.update(clock)
 
    # Go ahead and update the screen with what we've drawn.
    screen.blit(camera, (0, 0))
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
