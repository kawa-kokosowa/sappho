import os

import pygame

from sappho import collide, animate


class TestColliderSprite(object):

    # NOTE, TODO: this is a pretty bad test. Ideally, it
    # would do something more specific in addition to retesting
    # after the collision_sprite is updated, which should then
    # correspond to that position of the GIF/AnimatedSprite.
    def test_basic_attributes(self):
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

    def mock_sprite_group(self):
        pass

    def test_collides_rect(self):
        pass

    def test_collides_rect_mask(self):
        pass


# The below pattern can be used for collides_rect, collides_Rect_mask,
# try_to_move

# Create a group of sprites with various unique positions

# Create a sprite which will be checked for collisions
# against the group of sprites created in the last step.
# We intentionally place this collidersprite somewhere that'll
# collide with at least one colliddersprite from the group of
# the last step
