"""Camera control on a surface.

"""

import pygame


class CameraBehavior(object):
    """How a camera moves. How it handles boundaries,
    character movement, etc.

    You'll want to inherit this class when creating
    a CameraBehavior, including overriding the
    move method.

    """

    def __init__(self, camera):
        self.camera = camera

    # NOTE: You'll want to override this when you inherit.
    def move(self, focal_rectangle):
        """How the camera centers on an object.
        
        Note that simply putting the character directly
        in the center of the screen is _really bad_ but does have some 
        use cases.
        
        Arguments:
            focal_rectangle (pygame.Rect): Rectangle which
                is used to possibly adjust camera position.
            
        Returns:
            pygame.Rect: the view area, represented as a Pygame
                rectangle.

        """

        scroll_position = focal_rectangle.topleft
        position_rect = pygame.Rect(scroll_position,
                                    self.camera.camera_resolution)

        return position_rect


class CameraCenterBehavior(CameraBehavior):
    """A camera behavior that centers the
    focal rectangle on the screen.
    
    """

    def move(self, focal_rectangle):
        """Move the camera, keeping the focal rectangle
        in the center of the screen where possible.

        Arguments:
            focal_rectangle (pygame.Rect): Rectangle which
                is used to possibly adjust camera position.
            
        Returns:
            pygame.Rect: the view area, represented as a Pygame
                rectangle.

        """

        focal_x = (focal_rectangle.x
                   - (self.camera.camera_resolution[0] / 2) -
                   - (focal_rectangle.width / 2))
        focal_y = (focal_rectangle.y
                   - (self.camera.camera_resolution[1] / 2)
                   - (focal_rectangle.height / 2))

        if focal_x < 0:
            focal_x = 0
        if focal_y < 0:
            focal_y = 0
        if focal_x + self.camera.camera_resolution[0] > self.camera.source_resolution[0]:
            focal_x = self.camera.source_resolution[0] - self.camera.camera_resolution[0]
        if focal_y + self.camera.camera_resolution[1] > self.camera.source_resolution[1]:
            focal_y = self.camera.source_resolution[1] - self.camera.camera_resolution[1]

        position_rect = pygame.Rect((focal_x, focal_y),
                                    self.camera.camera_resolution)

        return position_rect

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

    def __init__(self, source_resolution, target_resolution, camera_resolution, behavior=None):
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

        self.view_rect = pygame.Rect((0, 0),
                                     self.camera_resolution)

        if behavior is None:
            self.behavior = CameraBehavior(self)
        else:
            self.behavior = behavior

    def update(self):
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

        subsurface = self.source_surface.subsurface(self.view_rect)
        scaled_surface = pygame.transform.scale(subsurface,
                                                self.target_resolution)

        # Blit the scaled surface to this camera (which is also a surface)
        super(Camera, self).blit(scaled_surface, (0, 0))

    def scroll_to(self, focal_rectangle):
        """Scroll to the given focal rectangle using the current behavior.

        """

        self.view_rect = self.behavior.move(focal_rectangle)
        self.update()

    def blit(self, surface, position):
        """ Blit the given surface to our source surface at the given 
        position.

        Arguments:
            surface (Surface): Surface to blit
            position (tuple[int, int]): Position to blit to
        """

        self.source_surface.blit(surface, position)
        self.update()
