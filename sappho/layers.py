import pygame


class SurfaceLayers(object):

    def __init__(self, target_surface, number_of_layers):
        self._target_surface = target_surface
        self._surface_layers = self.create_surface_layers(target_surface,
                                                          number_of_layers)

    @staticmethod
    def create_surface_layers(target_surface, number_of_layers):
        surface_layers = []

        for i in range(number_of_layers):
            surface = pygame.surface.Surface(target_surface.get_size(),
                                             pygame.SRCALPHA, 32)
            surface_layers.append(surface)

        return surface_layers

    def __getitem__(self, key):

        return self._surface_layers[key]

    def render(self):

        for surface in self._surface_layers:
            self._target_surface.blit(surface, (0, 0))

        target_surface = self._target_surface
        number_of_layers = len(self._surface_layers)
        self._surface_layers = self.create_surface_layers(target_surface,
                                                          number_of_layers)
