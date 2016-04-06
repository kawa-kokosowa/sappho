import os

import pygame

from .. import sappho
from .common import compare_surfaces


class TestSurfaceLayers(object):
    """

    Do not need to test create_surface_layers(), because
    it's inherent to SurfaceLayers' initialization and
    everything else tested.

    """

    NUMBER_OF_LAYERS = 100
    TARGET_SURFACE_SIZE = (800, 600)

    def setup(self):
        self.target_surface = pygame.surface.Surface(self.TARGET_SURFACE_SIZE)
        self.surface_layers = sappho.layers.SurfaceLayers(self.target_surface,
                                                   self.NUMBER_OF_LAYERS)

    def test_getitem(self):

        for i in range(self.NUMBER_OF_LAYERS):
            self.surface_layers[i]

    def test_len(self):
        assert len(self.surface_layers) == self.NUMBER_OF_LAYERS

    def test_iter(self):

        for i, surface in enumerate(self.surface_layers):
            assert surface is self.surface_layers[i]

        assert i == (self.NUMBER_OF_LAYERS - 1)

    def test_sizes(self):

        for surface in self.surface_layers:
            assert surface.get_size() == self.TARGET_SURFACE_SIZE

    def test_render(self):

        subsurface_size = (150, 150)

        # Create our test surfaces
        background = pygame.surface.Surface(self.TARGET_SURFACE_SIZE)
        rect1 = pygame.surface.Surface(subsurface_size)
        rect1pos = (100, 100)
        rect2 = pygame.surface.Surface(subsurface_size)
        rect2pos = (200, 200)
        rect3 = pygame.surface.Surface(subsurface_size)
        rect3pos = (300, 300)

        # Fill the surfaces
        background.fill((255, 255, 255))
        rect1.fill((255, 0, 0))
        rect2.fill((0, 255, 0))
        rect3.fill((0, 0, 255))

        # Create a surface to compare with and blit our test surfaces
        test_surface = pygame.surface.Surface(self.TARGET_SURFACE_SIZE)
        test_surface.blit(background, (0, 0))
        test_surface.blit(rect1, rect1pos)
        test_surface.blit(rect2, rect2pos)
        test_surface.blit(rect3, rect3pos)

        # Create the SurfaceLayers object and fill it with our layers
        surface_layers = sappho.layers.SurfaceLayers(self.target_surface, 4)
        surface_layers[0].blit(background, (0, 0))
        surface_layers[1].blit(rect1, rect1pos)
        surface_layers[2].blit(rect2, rect2pos)
        surface_layers[3].blit(rect3, rect3pos)

        # Render to the target surface
        surface_layers.render()

        # Compare the two surfaces
        assert(compare_surfaces(self.target_surface, test_surface))

