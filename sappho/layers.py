import pygame


class SurfaceLayers(object):
    """Ordered series of pygame surfaces the size
    of the target surface it draws each layer on.

    """

    def __init__(self, target_surface, number_of_layers):
        """Create the surface layers and store the target
        surface to draw to.

        Arguments:
            target_surface (pygame.surface.Surface): This is
                used for two things: setting the size of the
                layer surfaces to be created, and secondly this
                surface has each layer drawn to it every render().
            number_of_layers (int): How many surface layers to
                generate?

        """

        self._target_surface = target_surface
        self._surface_layers = self.create_surface_layers(target_surface,
                                                          number_of_layers)

    @staticmethod
    def create_surface_layers(target_surface, number_of_layers):
        """Create a list of pygame surfaces
        the size of the target surface.

        Arguments:
            target_surface (pygame.surface.Surface): The surface
                whose dimensions will be used for each layer.
            number_of_layers (int): The number of surfaces to
                create/return.

        Return:
            list[pygame.surface.Surface]

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

        Return:
            pygame.surface.Surface: The surface belonging
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
        """Draw each layer onto the target surface.

        Note:
            Draws in the same order found in
            self._surface_layers.

        """

        for surface in self._surface_layers:
            self._target_surface.blit(surface, (0, 0))

        target_surface = self._target_surface
        number_of_layers = len(self._surface_layers)
        self._surface_layers = self.create_surface_layers(target_surface,
                                                          number_of_layers)
