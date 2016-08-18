import os

import pygame

from sappho import collide, animate


class TestColliderSprites(object):

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
