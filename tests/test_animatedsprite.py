import os

import pygame

from .. import sappho
from ..sappho.animatedsprite import Frame


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
        animsprite = sappho.AnimatedSprite.from_file(path)

        # Create surfaces to compare against
        frameone = pygame.surface.Surface((10, 10))
        frameone.fill((255, 0, 0))
        frametwo = pygame.surface.Surface((10, 10))
        frametwo.fill((0, 255, 0))

        # Blit the AnimatedSprite (which should give us our first frame)
        outputsurface = pygame.surface.Surface((10, 10))
        outputsurface.blit(animsprite.image, (0, 0))

        output_view = outputsurface.get_view()
        frameone_view = frameone.get_view()

        assert(output_view.raw == frameone_view.raw)

        del output_view
        del frameone_view
        del outputsurface

        # Update the AnimatedSprite
        animsprite.update(clock)

        # Blit again, which should give us our second frame
        outputsurface = pygame.surface.Surface((10, 10))
        outputsurface.blit(animsprite.image, (0, 0))

        output_view = outputsurface.get_view()
        frametwo_view = frametwo.get_view()

        assert(output_view.raw == frametwo_view.raw)

        del output_view
        del frametwo_view
        del outputsurface


    def test_animation(self):
        # Create two surfaces with different colors
        frameone_surface = pygame.surface.Surface((10, 10))
        frameone_surface.fill((255, 0, 0))
        frametwo_surface = pygame.surface.Surface((10, 10))
        frametwo_surface.fill((0, 255, 0))

        # Create frames from these surfaces
        frameone = Frame(frameone_surface, 0, 1000)
        frametwo = Frame(frametwo_surface, 1000, 2000)

        # Create a mock Clock object for the AnimatedSprite
        clock = MockClock()

        # Create the AnimatedSprite with our frames
        animsprite = sappho.AnimatedSprite([frameone, frametwo])

        # Blit the AnimatedSprite (which should give us our first frame)
        outputsurface = pygame.surface.Surface((10, 10))
        outputsurface.blit(animsprite.image, (0, 0))

        output_view = outputsurface.get_view()
        frameone_view = frameone_surface.get_view()

        assert(output_view.raw == frameone_view.raw)

        del output_view
        del frameone_view
        del outputsurface

        # Update the AnimatedSprite
        animsprite.update(clock)

        # Blit again, which should give us our second frame
        outputsurface = pygame.surface.Surface((10, 10))
        outputsurface.blit(animsprite.image, (0, 0))

        output_view = outputsurface.get_view()
        frametwo_view = frametwo_surface.get_view()

        assert(output_view.raw == frametwo_view.raw)

        del output_view
        del frametwo_view
        del outputsurface
