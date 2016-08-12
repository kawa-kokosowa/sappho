"""Demo pygame game using Sappho.

A very horrible and basic pygame game which
utilizes Sappho (hopefully) to the fullest and
acts as a test.

This could also serve as a template in the future.

Needs to use sprite groups.

"""
 
import random

import pygame

from sappho.collide import CollisionSprite, Collision
from sappho.animate import AnimatedSprite
from sappho.tiles import TileMap, Tilesheet, tmx_file_to_tilemaps
from sappho.layers import SurfaceLayers
from sappho.camera import Camera, CameraCenterBehavior

import config

# init pygame
pygame.mixer.init(22100, -16, 2, 64)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

THIP_SOUND = pygame.mixer.Sound("thip.ogg")
SMALL_EXPLODE_SOUND = pygame.mixer.Sound("smallexplode.ogg")
CRUSH_SOUND = pygame.mixer.Sound("crush.ogg")


class Asteroid(CollisionSprite):
    COLOR = GREEN

    def __init__(self, center, size, x_speed, y_speed):
        image = pygame.Surface([size, size])
        self.rect = image.get_rect()
        self.rect.center = center
        self.image = image
        self.image.fill(self.COLOR)
        self.x_speed = x_speed
        self.y_speed = y_speed
        super(Asteroid, self).__init__(self)

    def new_smaller_asteroid(self):
        """New x and y speed based on player coords

        """

        new_asteroid_x_speed = random.choice([1, -1])
        new_asteroid_y_speed = random.choice([1, -1])

        new_asteroid_size = self.rect.width / 2
        new_asteroid = Asteroid(self.rect.center,
                                new_asteroid_size,
                                new_asteroid_x_speed,
                                new_asteroid_y_speed)
        return new_asteroid

    def explode(self, asteroid_list):
        """Explode into as many pieces as ... size

        """

        if self.rect.width > 3:

            for i in range(self.rect.width / 2):
                new_asteroid = self.new_smaller_asteroid()
                asteroid_list.add(new_asteroid)

        SMALL_EXPLODE_SOUND.play()
        asteroid_list.remove(self)

    def update(self, wall_list, layer_size, asteroid_list, player_bullet_list, timedelta):
        self.rect.topleft = (self.rect.left + self.x_speed,
                             self.rect.top + self.y_speed)

        new_rect = wrap_logic(self.rect, layer_size)
        self.rect = new_rect
        collision_bullet = self.collides_with_any_in_group(player_bullet_list)

        if collision_bullet:

            if self.rect.width >= 4:
                self.explode(asteroid_list)

            player_bullet_list.remove(collision_bullet)
             
        # colliding with wall?
        collision_wall = self.collides_with_any_in_group(wall_list)

        if collision_wall:
            self.explode(asteroid_list)


class Bullet(CollisionSprite):

    def __init__(self, duration, color, center, x_speed, y_speed, size):
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.current_duration = 0
        self.total_duration = duration
        super(Bullet, self).__init__(self)

    def update(self, player_bullet_list, wall_list, timedelta):
        self.current_duration += timedelta

        if self.current_duration >= self.total_duration:
            player_bullet_list.remove(self)

        self.rect.topleft = (self.x_speed + self.rect.left,
                             self.y_speed + self.rect.top)

        # now we must see if we collide
        collision_wall = self.collides_with_any_in_group(wall_list)

        if collision_wall:
            player_bullet_list.remove(self)
            THIP_SOUND.play()


def wrap_logic(rect, layer_size):
    new_rect = rect.copy()

    if new_rect.centery > layer_size[1]:
        new_rect.centery -= layer_size[1]
    elif new_rect.centery < 0:
        new_rect.centery += layer_size[1]

    if new_rect.centerx > layer_size[0]:
        new_rect.centerx -= layer_size[0]
    elif new_rect.centerx < 0:
        new_rect.centerx += layer_size[0]

    return new_rect


# Setup #######################################################################
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

# a background animation
# will be paralax
animated_bg = AnimatedSprite.from_gif("bg.gif")

# The sprite which the player controls
player_sprite = AnimatedSprite.from_gif(config.ANIMATED_SPRITE_PATH, mask_threshold=127)
player_collider = CollisionSprite(player_sprite)
player_collider.topleft = config.START_POSITION

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
camera = Camera(surface_size, config.RESOLUTION, config.VIEWPORT,
                behavior=CameraCenterBehavior())

# The render layers which we draw to
layers = SurfaceLayers(camera.source_surface, len(tilemap_surfaces))

# For bullets
player_bullet_list = pygame.sprite.Group()

# Asteroids
asteroid_list = pygame.sprite.Group()

# how far we can shoot is based on if player is mounted or not
bullet_duration = 200
bullet_color = BLUE
bullet_size = (2, 2)

# Main program loop ###########################################################
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
                x_speed = max([x_speed - 1, -config.MAX_SPEED])
            elif event.key == pygame.K_RIGHT:
                x_speed = min([x_speed + 1, config.MAX_SPEED])
            elif event.key == pygame.K_UP:
                y_speed = max([y_speed - 1, -config.MAX_SPEED])
            elif event.key == pygame.K_DOWN:
                y_speed = min([y_speed + 1, config.MAX_SPEED])
            elif event.key == pygame.K_d:
                CRUSH_SOUND.play()
                bullet = Bullet(bullet_duration, bullet_color, player_collider.rect.center, 4, 0, bullet_size)
                player_bullet_list.add(bullet)
            elif event.key == pygame.K_a:
                CRUSH_SOUND.play()
                bullet = Bullet(bullet_duration, bullet_color, player_collider.rect.center, -4, 0, bullet_size)
                player_bullet_list.add(bullet)
            elif event.key == pygame.K_s:
                CRUSH_SOUND.play()
                bullet = Bullet(bullet_duration, bullet_color, player_collider.rect.center, 0, 4, bullet_size)
                player_bullet_list.add(bullet)
            elif event.key == pygame.K_w:
                CRUSH_SOUND.play()
                bullet = Bullet(bullet_duration, bullet_color, player_collider.rect.center, 0, -4, bullet_size)
                player_bullet_list.add(bullet)

    # Test if the player is going to collide with any other objects
    # and if not, move the player

    # Move the object according to the speed vector.
    #
    # We will be resetting player_collider.rect.topleft
    # to old_topleft if there is a collision.
    tilemap_on_players_index = tilemaps_by_layer[config.ANIMATED_SPRITE_Z_INDEX]
    collision_group_on_player_index = tilemap_on_players_index.collision_group

    if x_speed != 0 or y_speed != 0:
        layer_size = layers[0].get_size()

        new_coord = [x_speed + player_collider.rect.topleft[0],
                     y_speed + player_collider.rect.topleft[1]]
        dummy_rect = player_collider.rect.copy()
        dummy_rect.topleft = new_coord
        new_coord = wrap_logic(dummy_rect, layer_size).topleft

        # try range preceeding
        # could be a "Find nearest to obstruction"
        try:
            player_collider.try_to_move(new_coord, collision_group_on_player_index)
            bullet_duration = 200
            bullet_size = (2, 2)
            bullet_color = BLUE
        except Collision:
            THIP_SOUND.play()
            bullet_duration = 500
            bullet_color = RED
            bullet_size = (4, 4)
            collided_at_this_y_speed = y_speed
            collided_at_this_x_speed = x_speed
            x_speed = 0
            y_speed = 0       

            if collided_at_this_y_speed > 0:
                y_modifier = -1
            elif collided_at_this_y_speed < 0:
                y_modifier = 1
            elif collided_at_this_y_speed == 0:
                y_modifer = 0

            if collided_at_this_x_speed > 0:
                x_modifier = -1
            elif collided_at_this_x_speed < 0:
                x_modifier = 1
            elif collided_at_this_x_speed == 0:
                x_modifer = 0

            while not (collided_at_this_x_speed == 0 and collided_at_this_y_speed == 0):

                if collided_at_this_x_speed != 0:
                    collided_at_this_x_speed += x_modifier

                if collided_at_this_y_speed != 0:
                    collided_at_this_y_speed += y_modifier

                new_coord = [collided_at_this_x_speed + player_collider.rect.topleft[0],
                             collided_at_this_y_speed + player_collider.rect.topleft[1]]

                try:
                    player_collider.try_to_move(new_coord, collision_group_on_player_index)
                except Collision:
                    pass
                else:
                    camera.scroll_to(player_collider.rect)
                    break

        else:
            camera.scroll_to(player_collider.rect)
 
    # create some asteroids, hurdled t the player
    # we should make these chase the player, actually...
    if len(asteroid_list) < 3:
        plus_or_minus_x = random.choice([1, -1])
        new_asteroid_x = (player_collider.rect.top - (20 * plus_or_minus_x) * plus_or_minus_x)
        plus_or_minus_y = random.choice([1, -1])
        new_asteroid_y = (player_collider.rect.left - (20 * plus_or_minus_y) * plus_or_minus_y)
        another_asteroid = Asteroid((new_asteroid_x, new_asteroid_y), 10, 0, 1)
        asteroid_list.add(another_asteroid)

    # DRAWING/RENDER CODE

    # first let's render each tilemap on its respective surface
    for i, tilemap_layer in enumerate(tilemap_surfaces):
        layers[i].blit(animated_bg.image, camera.view_rect.topleft)
        layers[i].blit(tilemap_layer, (0, 0))


    # Finally let's render the animated sprite on some
    # arbitrary layer. In the future the TMX will set this.
    layers[config.ANIMATED_SPRITE_Z_INDEX].blit(player_sprite.image,
                                                player_collider.rect.topleft)

    # draw asteroids
    asteroid_list.draw(layers[config.ANIMATED_SPRITE_Z_INDEX])
    # draw bullets
    player_bullet_list.draw(layers[config.ANIMATED_SPRITE_Z_INDEX])

    # ... Draw those layers!
    layers.render()
     
    # Let's get the timedelta and then send it to the appropriate things...
    timedelta = clock.get_time()
    camera.update_state("hahahahahah lies lies lies")
    player_sprite.update(timedelta)
    animated_bg.update(timedelta)
    player_bullet_list.update(player_bullet_list, collision_group_on_player_index, timedelta)
    asteroid_list.update(collision_group_on_player_index, layers[0].get_size(), asteroid_list, player_bullet_list, timedelta)
 
    # Go ahead and update the screen with what we've drawn.
    screen.blit(camera, (0, 0))
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
