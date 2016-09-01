from __future__ import absolute_import

import pygame
import pytest

from sappho.camera import (Camera,
                           CameraBehavior,
                           CameraCenterBehavior,
                           CameraOutOfBounds)

from .common import compare_surfaces


class TestCameraBehavior(object):

    def test_out_of_bounds(self):
        """Test the CameraOutOfBounds exception through
        testing through the default camera behavior movement.

        1. Create a camera
        2. Create a rectangle whose topleft is out-of-bounds
           of the Camera source surface.
        3. Assert exception is raised!

        """

        camera = Camera((800, 600), (1080, 1050), (300, 300))

        out_of_bounds_coord = (2000, 2000)
        out_of_bounds_rect = pygame.Rect(out_of_bounds_coord, [32, 32])

        with pytest.raises(CameraOutOfBounds):
            camera.scroll_to(out_of_bounds_rect)
            camera.update_state(28974329)

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
        camera.update_state(["this", "seriously", 323423, "works"])

        # Set focus to the top left pixel and check that we have a 2x2
        # view into the test surface in the top left (that is, (0, 0)
        # to (1, 1) should be visible)
        camera.scroll_to(pygame.Rect(0, 0, 1, 1))
        camera.update_state("HAHA LIES THIS IS LIES AHAHAHA")
        focal_subsurface = test_surface.subsurface(pygame.Rect(0, 0, 2, 2))
        assert(compare_surfaces(focal_subsurface, camera))

        # Set focus to the pixel in the center of the test surface (1, 1)
        # and check that (1, 1) to (2, 2) is displayed on the camera
        camera.scroll_to(pygame.Rect(1, 1, 1, 1))
        camera.update_state("lialskdjflasjflksadjf")
        focal_subsurface = test_surface.subsurface(pygame.Rect(1, 1, 2, 2))
        assert(compare_surfaces(focal_subsurface, camera))


class TestCameraCenterBehavior(object):
    """Notably does not raise exception
    when out-of-bounds.

    """

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
        camera.update_state("AFSDALJASD;LKJFASD0000LOLOL")

        # Scroll to the first focus position (top left)
        camera.scroll_to(pygame.Rect(0, 0, 1, 1))
        camera.update_state({"this": "value don't mattah", 1: 'lol'})

        # Take a subsurface of test_surface that should represent the
        # camera's current view and compare the camera to it
        focal_subsurface = test_surface.subsurface(pygame.Rect(0, 0, 3, 3))
        assert(compare_surfaces(focal_subsurface, camera))

        # Move the focus to the center of the surface and compare the view
        # again to the current subsurface
        camera.scroll_to(pygame.Rect(3, 3, 1, 1))
        camera.update_state(['o', ('x', 2), 3])
        focal_subsurface = test_surface.subsurface(pygame.Rect(2, 2, 3, 3))
        assert(compare_surfaces(focal_subsurface, camera))

        # Move the focus to the bottom right of the surface
        # and compare the view again.
        camera.scroll_to(pygame.Rect(5, 5, 1, 1))
        camera.update_state("lol")
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
        camera.source_surface.blit(red_surface, (0, 0))
        camera.source_surface.blit(blue_surface, (1, 0))
        camera.update_state("so many of these")

        # We should be at (0, 0) so blitting should get us a red pixel
        output_surface.blit(camera, (0, 0))
        assert(compare_surfaces(red_surface, output_surface))

        # Scroll one pixel to the left, and we should get a blue pixel
        # when blitting
        focal_rect = pygame.Rect((1, 0), (1, 1))
        camera.scroll_to(focal_rect)  # updates for us
        camera.update_state("just a lot")
        output_surface.blit(camera, (0, 0))
        assert(compare_surfaces(blue_surface, output_surface))

    # FIXME: This is messy!
    def test_scale(self):
        # Create surface to render to (screen mock)
        mock_screen = pygame.surface.Surface((10, 10))

        # Create fixtures (a 1x1 red square, and a 10x10 red square)
        red_small = pygame.surface.Surface((1, 1))  # native/unscale
        red_large = pygame.surface.Surface((10, 10))  # to-scale/scaled
        red_small.fill((255, 0, 0))
        red_large.fill((255, 0, 0))

        # Create the camera with scaling enabled and blit our red pixel to it
        camera = Camera((1, 1), (10, 10), (1, 1))
        camera.source_surface.blit(red_small, (0, 0))
        camera.update_state(340)

        # Blit and compare
        # Draw the to-scale camera surface to the screen mock
        mock_screen.blit(camera, (0, 0))
        assert compare_surfaces(mock_screen, red_large)
