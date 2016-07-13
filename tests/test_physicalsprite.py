import pygame

from ..sappho import physicalsprite, animatedsprite


class TestPhysicalSprites(object):

    # NOTE, TODO: this is a pretty bad test. Ideally, it
    # would do something more specific in addition to retesting
    # after the physical_sprite is updated, which should then
    # correspond to that position of the GIF/AnimatedSprite.
    def test_basic_attributes(self):
        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "animatedsprite.gif"))
        animsprite = animatedsprite.AnimatedSprite.from_gif(path,
                                                            mask_threshold=254)
        physical_sprite = physicalsprite.PhysicalSprite(animsprite)

        assert physical_sprite.rect.size == (10, 10)
        assert hasattr(physical_sprite, 'mask')
        # TODO: should test after updating sprite
