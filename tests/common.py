import pygame


def compare_surfaces(pygame_surface_a, pygame_surface_b):
    """Compare two Pygame surfaces, assuring they are
    exactly the same.

    Arguments:
        pygame_surface_a (pygame.Surface):
        pygame_surface_b (pygame.Surface):

    Returns:
        bool: True if the surfaces are the same, False
            if the surfaces are different.

    """

    surface_a_pixelarray = pygame.PixelArray(pygame_surface_a)
    surface_b_pixelarray = pygame.PixelArray(pygame_surface_b)

    return surface_a_pixelarray.compare(surface_b_pixelarray)
