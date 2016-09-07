import os

import pygame

from sappho import collide

testpath = os.path.realpath(__file__)
path = os.path.abspath(os.path.join(testpath,
                                    "..",
                                    "resources",
                                    "animatedsprite.gif"))
animsprite = animate.AnimatedSprite.from_gif(path,
                                             mask_threshold=254)
collision_sprite = collide.ColliderSprite(animsprite)

assert collision_sprite.rect.size == (10, 10)
assert hasattr(collision_sprite, 'mask')
# TODO: should test after updating sprite

# The below pattern can be used for collides_rect, collides_Rect_mask,
# try_to_move

# Create a group of sprites with various unique positions

# Create a sprite which will be checked for collisions
# against the group of sprites created in the last step.
# We intentionally place this collidersprite somewhere that'll
# collide with at least one colliddersprite from the group of
# the last step
