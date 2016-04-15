import sys
import pygame

PY3 = sys.version_info[0] == 3
range = range if PY3 else xrange


class SurfaceLayers(object):
    """Ordered series of pygame surfaces, each the size of the target
    surface given at creation time.

    Arguments:
        target_surface (pygame.Surface): Surface that will have
            have the layers blitted to when render() is called. The size
            of this surface is used as the size of the generated layers.
        number_of_layers (int): Number of layers to generate.

    """

    def __init__(self, target_surface, number_of_layers):
        self._target_surface = target_surface
        self._surface_layers = self.create_surface_layers(target_surface,
                                                          number_of_layers)

    @staticmethod
    def create_surface_layers(target_surface, number_of_layers):
        """Create a list of pygame surfaces
        the size of the target surface.

        Arguments:
            target_surface (pygame.Surface): The surface
                whose dimensions will be used for each layer.
            number_of_layers (int): The number of surfaces to
                create/return.

        Returns:
            list[pygame.Surface]: List of surfaces

        """

        surface_layers = []

        for i in range(number_of_layers):
            surface = pygame.surface.Surface(target_surface.get_size(),
                                             pygame.SRCALPHA, 32)
            surface_layers.append(surface)

        return surface_layers

    def __getitem__(self, key):
        """Access a surface by z-index.

        Arguments:
            key (int): The z-index of the surface.

        Raises:
            IndexError: When the z-index is invalid.

        Returns:
            pygame.Surface: The surface belonging
                to the z-index specified.

        """

        return self._surface_layers[key]

    def __len__(self):
        """Return the number of layers.

        Returns:
            int: Number of members in self.surface_layers.

        """

        return len(self._surface_layers)

    def __iter__(self):
        """Iterate through the surface layers.

        Yields:
            pygame.surface.Surface

        """

        for surface in self._surface_layers:
            yield surface

    def render(self):
        """Draw each layer onto the target surface in the correct order.

        """

        for surface in self._surface_layers:
            self._target_surface.blit(surface, (0, 0))

        target_surface = self._target_surface
        number_of_layers = len(self._surface_layers)
        self._surface_layers = self.create_surface_layers(target_surface,
                                                          number_of_layers)
