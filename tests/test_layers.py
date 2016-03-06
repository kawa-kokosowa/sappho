import os

import pygame

from .. import sappho


class TestSurfaceLayers(object):
    """

    Do not need to test create_surface_layers(), because
    it's inherent to SurfaceLayers' initialization and
    everything else tested.

    """

    NUMBER_OF_LAYERS = 100
    TARGET_SURFACE_SIZE = (800, 600)

    def setup(self):
        target_surface = pygame.surface.Surface(self.TARGET_SURFACE_SIZE)
        self.surface_layers = sappho.SurfaceLayers(target_surface,
                                                   self.NUMBER_OF_LAYERS)

    def test_getitem(self):

        for i in range(self.NUMBER_OF_LAYERS):
            self.surface_layers[i]

    def test_len(self):
        assert len(self.surface_layers) == self.NUMBER_OF_LAYERS

    def test_iter(self):

        for i, surface in enumerate(self.surface_layers):
            assert surface is self.surface_layers[i]

        assert i == (NUMBER_OF_LAYERS - 1)

    def test_sizes(self):

        for surface in self.surface_layers:
            assert surface.get_size() == self.TARGET_SURFACE_SIZE

    def test_render(self):
        """This requires a fixture.

        """

        pass
