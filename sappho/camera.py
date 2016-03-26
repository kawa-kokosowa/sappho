"""Camera control on a surface.

"""

import pygame


# NOTE: this is merely scaffolding to get
# some ideas across!
class CameraBehavior(object):
    """How a camera moves. How it handles boundaries,
    character movement, etc.

    """

    def center_on(some_object):
        """How the camera centers on an object.
        
        Note that simply putting the character directly
        in the center of the screen is _really bad_.

        That noted, the name could use some work.
        
        """

        pass


class Camera(pygame.surface.Surface):
    """Surface that acts as a scrollable view, with optional scaling
    onto another surface.

    Arguments:
        source_resolution (tuple[int, int]): The overal dimensions
            of the environment the camera is panning over.
        target_resolution (tuple[int, int]): Resolution to scale up the
            view of the surface to
        camera_resolution (tuple[int, int]): Resolution of the view onto
            the source surface

    """

    def __init__(self, source_resolution, target_resolution, camera_resolution):
        """

        Arguments:
            source_resolution (tuple[int, int]): Maximal size of the
                environment being portrayed. Imagine a map with
                many inconsistently-sized layers. You'd want the
                source_resolution of the camera to be what the
                aformentioned map's dimensions would be if everything
                were just flattened to a single, new layer. Anything
                beyond the specified resolution will not be on camera!

        """

        super(Camera, self).__init__(target_resolution)

        self.source_surface = pygame.surface.Surface(source_resolution,
                                                     pygame.SRCALPHA)
        self.source_resolution = source_resolution
        self.target_resolution = target_resolution
        self.camera_resolution = camera_resolution
        self.scroll_position = (0, 0)

    def _update(self):
        """Update the Camera to point to the
        current scroll position.

        Gets the "view" from the current scroll position
        and camera resolution. That view is used to create
        a subsurface of the "source subsurface," scaled to
        the target_resolution. The new subsurface is then
        blit to the camera (which is a surface, itself!).

        Warning:
            This should only be used internally, to scroll
            use the scroll() or scroll_absolute() functions.

        """

        position_rect = pygame.Rect(self.scroll_position,
                                    self.camera_resolution)
        subsurface = self.source_surface.subsurface(position_rect)

        scaled_surface = pygame.transform.scale(subsurface,
                                                self.target_resolution)

        # Blit the scaled surface to this camera (which is also a surface)
        super(Camera, self).blit(scaled_surface, (0, 0))

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
