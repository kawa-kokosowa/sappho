import os

import pygame

from .. import sappho


class TestSurfaceLayers(object):
    NUMBER_OF_LAYERS = 100
    TARGET_SURFACE_SIZE = (800, 600)

    def setup(self):
        self.target_surface = pygame.surface.Surface(self.TARGET_SURFACE_SIZE)
        self.surface_layers = sappho.SurfaceLayers(self.target_surface,
                                                   self.NUMBER_OF_LAYERS)

    def test_getitem(self):

        for i in range(self.NUMBER_OF_LAYERS):
            self.surface_layers[i]

    def test_len(self):
        assert len(self.surface_layers) == self.NUMBER_OF_LAYERS

    def test_iter(self):

        for i, surface in enumerate(self.surface_layers):
            assert surface is self.surface_layers[i]

        assert i == 99

    def test_sizes(self):

        for surface in self.surface_layers:
            assert surface.get_size() == self.TARGET_SURFACE_SIZE

    def test_render(self):

        subsurface_size = (self.TARGET_SURFACE_SIZE[0] / 2,
                           self.TARGET_SURFACE_SIZE[1] / 2)

        # Create our test surfaces
        background = pygame.surface.Surface(self.TARGET_SURFACE_SIZE)
        top_left = pygame.surface.Surface(subsurface_size)
        top_right = pygame.surface.Surface(subsurface_size)
        bottom_left = pygame.surface.Surface(subsurface_size)

        # Fill the surfaces
        background.fill((255, 255, 255))
        top_left.fill((255, 0, 0))
        top_right.fill((0, 255, 0))
        bottom_left.fill((0, 0, 255))

        # Create a surface to compare with and blit our test surfaces
        test_surface = pygame.surface.Surface(self.TARGET_SURFACE_SIZE)
        test_surface.blit(background, (0, 0))
        test_surface.blit(top_left, (0, 0))
        test_surface.blit(top_right, (subsurface_size[0], 0))
        test_surface.blit(bottom_left, (0, subsurface_size[1]))

        # Create the SurfaceLayers object and fill it with our layers
        surface_layers = sappho.SurfaceLayers(self.target_surface, 4)
        surface_layers[0].blit(background, (0, 0))
        surface_layers[1].blit(top_left, (0, 0))
        surface_layers[2].blit(top_right, (subsurface_size[0], 0))
        surface_layers[3].blit(bottom_left, (0, subsurface_size[1]))

        # Render to the target surface
        surface_layers.render()

        # Compare the two surfaces
        target_view = self.target_surface.get_view().raw
        test_view = test_surface.get_view().raw

        for i, pixel in enumerate(target_view):
            assert(pixel == test_view[i])
