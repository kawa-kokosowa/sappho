import os

import pygame

from ..sappho import Camera
from .common import compare_surfaces


class TestCamera(object):

    def test_scroll(self):
        # Create surface to render to
        output_surface = pygame.surface.Surface((1, 1))

        # Create fixtures
        red_surface = pygame.surface.Surface((1, 1))
        blue_surface = pygame.surface.Surface((1, 1))
        red_surface.fill((255, 0, 0))
        blue_surface.fill((0, 255, 0))

        # Create the camera and blit colors to it
        camera = Camera((2, 1), (1, 1), (1, 1))
        camera.blit(red_surface, (0, 0))
        camera.blit(blue_surface, (1, 0))

        # We should be at (0, 0) so blitting should get us a red pixel
        output_surface.blit(camera, (0, 0))
        assert(compare_surfaces(red_surface, output_surface))

        # Scroll one pixel to the left, and we should get a blue pixel
        # when blitting
        camera.scroll(1, 0)
        output_surface.blit(camera, (0, 0))
        assert(compare_surfaces(blue_surface, output_surface))

    def test_scale(self):
        # Create surface to render to
        output_surface = pygame.surface.Surface((10, 10))

        # Create fixtures
        red_small = pygame.surface.Surface((1, 1))
        red_large = pygame.surface.Surface((10, 10))
        red_small.fill((255, 0, 0))
        red_large.fill((255, 0, 0))

        # Create the camera with scaling enabled and blit our red pixel to it
        camera = Camera((1, 1), (10, 10), (1, 1))
        camera.blit(red_small, (0, 0))

        # Blit and compare
        output_surface.blit(camera, (0, 0))
        assert(compare_surfaces(output_surface, red_large))
