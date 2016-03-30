"""Camera control on a surface.

"""

import pygame


class CameraBehavior(object):
    """How a camera moves. How it handles boundaries,
    character movement, etc.

    This CameraBehavior, the default, keeps the focal rectangle
    in the top left of the camera view.

    You'll want to inherit this class when creating
    a CameraBehavior, including overriding the
    move method.

    Parameters:
        camera (sappho.Camera): The camera that this
            CameraBehavior belongs to.

    """

    def __init__(self, camera):
        self.camera = camera

    # NOTE: You'll want to override this when you inherit.
    def move(self, focal_rectangle):
        """Move the camera, keeping the focal rectangle in
        the top left of the camera view.

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

    Parameters:
        camera (sappho.Camera): The camera that this
            CameraBehavior belongs to.

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
        source_resolution (tuple[int, int]): Maximum size of the
            environment being portrayed. If you have a map with many
            inconsistently sized layers, this should be the size of 
            all of those layers flattened onto a single new layer.
            Anything beyond this size will not be on camera.
        target_resolution (tuple[int, int]): Resolution to scale up the
            view of the surface to
        camera_resolution (tuple[int, int]): Resolution of the view onto
            the source surface
        behavior (CameraBehavior): The initial behavior to use for this
            Camera.

    Attributes:
        behavior: The :py:class:`CameraBehavior <sappho.CameraBehavior>`
            that this Camera uses to control movement.

    """

    def __init__(self, source_resolution, target_resolution, camera_resolution, behavior=None):
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

        """

        subsurface = self.source_surface.subsurface(self.view_rect)
        scaled_surface = pygame.transform.scale(subsurface,
                                                self.target_resolution)

        # Blit the scaled surface to this camera (which is also a surface)
        super(Camera, self).blit(scaled_surface, (0, 0))

    def scroll_to(self, focal_rectangle):
        """Scroll to the given focal rectangle using the current behavior.

        Parameters:
            focal_rectangle (pygame.Rect): Rectangle to possibly update
                the view position to using the camera's current behavior

        """

        self.view_rect = self.behavior.move(focal_rectangle)
        self.update()
