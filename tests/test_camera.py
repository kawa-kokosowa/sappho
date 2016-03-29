import os

import pygame

from ..sappho import (Camera,
                      CameraBehavior,
                      CameraCenterBehavior)

from .common import compare_surfaces


class TestCameraCenterBehavior(object):
    def test_movement(self):
        """Test that moving the camera centers the focal rectangle on
        the screen. Creates a 7x7 surface, blitting red, green, and blue
        squares to it so they overlap, and checks that moving the camera
        focuses on the right place. 
        """

        # Create a surface and fill it with colored squares so that each
        # 3x3 view onto the surface is different
        test_surface = pygame.surface.Surface((7, 7))
        test_surface.fill((255, 0, 0), pygame.Rect(1, 1, 3, 3))
        test_surface.fill((0, 255, 0), pygame.Rect(2, 2, 3, 3))
        test_surface.fill((0, 0, 255), pygame.Rect(3, 3, 3, 3))

        # Set up our camera
        camera = Camera((7, 7), (3, 3), (3, 3))
        behavior = CameraCenterBehavior(camera)
        camera.behavior = behavior

        # Blit our test surface to the camera
        camera.source_surface.blit(test_surface, (0, 0))
        camera.update()

        # Scroll to the first focus position (top left)
        camera.scroll_to(pygame.Rect(0, 0, 1, 1))

        # Take a subsurface of test_surface that should represent the
        # camera's current view and compare the camera to it
        focal_subsurface = test_surface.subsurface(pygame.Rect(0, 0, 3, 3))
        assert(compare_surfaces(focal_subsurface, camera))

        # Move the focus to the center of the surface and compare the view
        # again to the current subsurface
        camera.scroll_to(pygame.Rect(3, 3, 1, 1))
        focal_subsurface = test_surface.subsurface(pygame.Rect(2, 2, 3, 3))
        assert(compare_surfaces(focal_subsurface, camera))

        # Move the focus to the bottom right of the surface and compare the view
        # again
        camera.scroll_to(pygame.Rect(5, 5, 1, 1))
        focal_subsurface = test_surface.subsurface(pygame.Rect(4, 4, 3, 3))
        assert(compare_surfaces(focal_subsurface, camera))


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
