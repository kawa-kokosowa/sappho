import os

import pygame

from ..sappho import animate
# this isn't very law of demeter...
from .common import compare_surfaces


class MockClock(object):
    def get_time(self):
        return 1000


class TestAnimatedSprite(object):

    def test_gif_loading(self):
        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "animatedsprite.gif"))

        # Create our mock clock
        clock = MockClock()

        # Create the AnimatedSprite object from the test GIF file
        animsprite = animate.AnimatedSprite.from_gif(path)

        # Test getting the dimensions of the largest frame
        assert animsprite.largest_frame_size() == (10, 10)

        # Create surfaces to compare against
        frameone = pygame.surface.Surface((10, 10))
        frameone.fill((255, 0, 0))
        frametwo = pygame.surface.Surface((10, 10))
        frametwo.fill((0, 255, 0))

        # Blit the AnimatedSprite (which should give us our first frame)
        outputsurface = pygame.surface.Surface((10, 10))
        outputsurface.blit(animsprite.image, (0, 0))

        assert(compare_surfaces(outputsurface, frameone))

        timedelta = clock.get_time()
        animsprite.update(timedelta)

        # Blit again, which should give us our second frame
        outputsurface = pygame.surface.Surface((10, 10))
        outputsurface.blit(animsprite.image, (0, 0))

        assert(compare_surfaces(outputsurface, frametwo))

    def test_animation(self):
        # Create two surfaces with different colors
        frameone_surface = pygame.surface.Surface((10, 10))
        frameone_surface.fill((255, 0, 0))
        frametwo_surface = pygame.surface.Surface((10, 10))
        frametwo_surface.fill((0, 255, 0))

        # Create frames from these surfaces
        frameone = animate.Frame(frameone_surface, 0, 1000)
        frametwo = animate.Frame(frametwo_surface, 1000, 2000)

        assert (frameone.__repr__()
                == "<Frame duration(1000) start_time(0) end_time(1000)>")

        # Create a mock Clock object for the AnimatedSprite
        clock = MockClock()

        # Create the AnimatedSprite with our frames
        animsprite = animate.AnimatedSprite([frameone, frametwo])

        # Blit the AnimatedSprite (which should give us our first frame)
        outputsurface = pygame.surface.Surface((10, 10))
        outputsurface.blit(animsprite.image, (0, 0))

        assert(compare_surfaces(outputsurface, frameone_surface))

        # Update the AnimatedSprite
        animsprite.update(clock.get_time())

        # Blit again, which should give us our second frame
        outputsurface = pygame.surface.Surface((10, 10))
        outputsurface.blit(animsprite.image, (0, 0))

        assert(compare_surfaces(outputsurface, frametwo_surface))
