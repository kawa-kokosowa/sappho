import os

import pygame

from ..sappho import (Camera,
                      CameraBehavior,
                      CameraCenterBehavior)

from .common import compare_surfaces


class TestCameraBehavior(object):

    def test_movement(self):
        # Create a test surface with a red square at (0, 0) and a blue
        # square at (1, 1), both being 2x2.
        test_surface = pygame.surface.Surface((3, 3))
        test_surface.fill((255, 0, 0), pygame.Rect(0, 0, 2, 2))
        test_surface.fill((0, 255, 0), pygame.Rect(1, 1, 2, 2))

        # Create our camera
        camera = Camera((3, 3), (2, 2), (2, 2),
                        behavior=CameraBehavior())

        # Blit our test surface
        camera.source_surface.blit(test_surface, (0, 0))
        camera.update()

        # Set focus to the top left pixel and check that we have a 2x2
        # view into the test surface in the top left (that is, (0, 0)
        # to (1, 1) should be visible)
        camera.scroll_to(pygame.Rect(0, 0, 1, 1))
        focal_subsurface = test_surface.subsurface(pygame.Rect(0, 0, 2, 2))
        assert(compare_surfaces(focal_subsurface, camera))

        # Set focus to the pixel in the center of the test surface (1, 1)
        # and check that (1, 1) to (2, 2) is displayed on the camera
        camera.scroll_to(pygame.Rect(1, 1, 1, 1))
        focal_subsurface = test_surface.subsurface(pygame.Rect(1, 1, 2, 2))
        assert(compare_surfaces(focal_subsurface, camera))


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
        camera = Camera((7, 7), (3, 3), (3, 3),
                        behavior=CameraCenterBehavior())

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
