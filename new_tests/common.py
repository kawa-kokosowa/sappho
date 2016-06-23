import itertools

import pygame


def _make_2d_list_of_size(width, height):
    a_2d_list = []

    for row in range(height):
        a_2d_list.append([None for i in range(width)])

    return a_2d_list


def _make_2d_color_list(pygame_surface):
    pygame_surface_size = pygame_surface.get_size()
    surface_width, surface_height = pygame_surface_size
    surface_2d_list_of_colors = _make_2d_list_of_size(*pygame_surface_size)

    for coordinate in itertools.product(range(0, surface_width),
                                        range(0, surface_height)):
        x, y = coordinate
        surface_2d_list_of_colors[y][x] = pygame_surface.get_at(coordinate)

    return surface_2d_list_of_colors


def compare_surfaces(pygame_surface_a, pygame_surface_b):
    """Compare two Pygame surfaces, assuring they are
    exactly the same.

    Arguments:
        pygame_surface_a (pygame.Surface):
        pygame_surface_b (pygame.Surface):

    Returns:
        bool: True if the surfaces are the same, 
            if the surfaces are different.

    """

    some_2d_color_list_a = _make_2d_color_list(pygame_surface_a)
    some_2d_color_list_b = _make_2d_color_list(pygame_surface_b)

    # TODO: check to make sure they're both the same size
    for y, row in enumerate(some_2d_color_list_a):

        for x, color in enumerate(row):

            if color != some_2d_color_list_b[y][x]:
                return False

    return True
