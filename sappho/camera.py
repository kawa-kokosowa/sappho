"""Camera control on a surface.

"""

import pygame


class Camera(pygame.surface.Surface):
    """ Surface that acts as a scrollable view, with optional scaling
    onto another surface.

    Arguments:
        source_resolution (tuple[int, int]):
        target_resolution (tuple[int, int]): Resolution to scale up the
            view of the surface to
        camera_resolution (tuple[int, int]): Resolution of the view onto
            the source surface
    """

    def __init__(self, source_resolution, target_resolution, camera_resolution):
        super(Camera, self).__init__(target_resolution)

        self.source_surface = pygame.surface.Surface(source_resolution,
                                                     pygame.SRCALPHA)

        self.source_res = source_resolution
        self.target_res = target_resolution
        self.camera_res = camera_resolution

        self.scroll_position = (0, 0)

    def _update(self):
        """ Update the Camera to point to the current scroll position.
        This should only be used internally, to scroll use the scroll()
        or scroll_absolute() functions.
        """

        position_rect = pygame.Rect(self.scroll_position, self.camera_res)
        subsurface = self.source_surface.subsurface(position_rect)

        scaledsurface = pygame.transform.scale(subsurface, self.target_res)

        super(Camera, self).blit(scaledsurface, (0, 0))

    def scroll(self, x, y):
        """ Scroll the view x pixels to the right and y pixels down.
        x and y can be negative, to signify scrolling left and up, respectively.

        Arguments:
            x (int): Number of pixels to scroll horizontally
            y (int): Number of pixels to scroll vertically.
        """

        self.scroll_position = (self.scroll_position[0] + x,
                                self.scroll_position[1] + y)

        self._update()

    def scroll_absolute(self, x, y):
        """ Scroll the view to an absolute position specified by x and y.

        Arguments: 
            x (int): X position to scroll to
            y (int): Y position to scroll to
        """

        self.scroll_position = (x, y)
        self._update()

    def blit(self, surface, position):
        """ Blit the given surface to our source surface at the given 
        position.

        Arguments:
            surface (Surface): Surface to blit
            position (tuple[int, int]): Position to blit to
        """

        self.source_surface.blit(surface, position)
        self._update()
