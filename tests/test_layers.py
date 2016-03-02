import os

import pygame

from .. import sappho


def test_layers():
    target_surface = pygame.surface.Surface([400, 300])
    surface_layers = sappho.SurfaceLayers(target_surface, 4)

    # Should use magic method that counts _surface_layers instead!
    assert len(surface_layers._surface_layers) == 4

    # should have __iter__ instead
    for surface in surface_layers._surface_layers:
        assert surface.get_size() == target_surface.get_size()

    surface_layers[0]
    surface_layers[1]
    surface_layers[2]
    surface_layers[3]
