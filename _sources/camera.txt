Camera and camera behaviors
===========================

.. py:module:: sappho.camera

Camera
------

The camera in Sappho allows you to have a small viewport onto the current
map and optionally scale it up to a larger resolution. This is useful, for
example, when you have a map with 10x10 pixel tiles, but you want the player's
view to fill an 800x600 pixel window but only allow viewing a part of
the map at a time.

.. autoclass:: Camera
   :members: scroll_to, update

Exceptions
----------

.. autoexception:: CameraOutOfBounds

Camera behaviors
----------------

Sappho's camera has switchable behaviors. These change which area of the
screen is visible depending on the focal :py:class:`pygame.Rect` that is 
given to the :py:meth:`Camera.scroll_to` method.

The default camera behavior, which is documented below, puts the focal
rectangle that is given in the top left corner of the view defined
by the :py:class:`Camera`.

.. autoclass:: CameraBehavior
   :members: move

Common camera behaviors
^^^^^^^^^^^^^^^^^^^^^^^

Sappho provides some camera behaviors that have some usefulness in common
games.

.. autoclass:: CameraCenterBehavior

Creating a custom camera behavior
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:func:`CameraBehavior.move` function, which should be overridden
when you subclass CameraBehavior, is called when the 
:py:func:`Camera.scroll_to` function is called to scroll the surface.

The move function is called with the :py:class:`pygame.Rect` that represents
the focal point of the view onto the source surface. It returns another
:py:class:`pygame.Rect` that represents the view onto the source surface
that should be displayed. The Rect can not go outside the bounds of the
source surface, as when the camera is updated, it creates a subsurface
of the source surface with the Rect that is returned by the move function.

The simplest implementation of a CameraBehavior would be to put the 
focal rectangle in the top left. This would be achieved by returning a
Rect that had the x and y attributes set to the x and y attributes of the
focal rectangle, with the width and height of the camera size (specified
by the ``camera_resolution`` property of the  :py:class:`Camera` that
is passed to the ``move`` method)::

    class TopLeftBehavior(CameraBehavior): 
        def move(self, camera, focal_rectangle):
            return pygame.Rect(focal_rectangle.topleft,
                               camera.camera_resolution)

Hovever, this does not constrain the view to the bounds of the source
surface, meaning that if the focal rectangle goes off the screen, or
it ventures into an area where the focal rectangle's X or Y position
plus the width of height of the view is greater than the width/height 
of the source surface, an error will occur because you can not create
a subsurface of the source surface that goes outside of the bounds of
the source surface. A :py:exc:`CameraOutOfBounds` exception is raised 
by the :py:func:`Camera.update` function if the Rect returned by the 
move function is out of bounds. This can be useful in some cases, but
for our case, we don't want to be able to go out of bounds, and instead
should constrain the bounds of the view to the surface::

    class TopLeftBehavior(CameraBehavior): 
        def move(self, camera, focal_rectangle):
            x = focal_rectangle.x
            y = focal_rectangle.y

            # Make sure we don't go off the top or left of the source surface
            if x < 0:
                x = 0
            if y < 0:
                y = 0

            # Make sure we don't go off the bottom or right of the source surface
            if x + camera.camera_resolution[0] > camera.source_resolution[0]:
                x = camera.source_resolution[0] - camera.camera_resolution[0]
            if y + camera.camera_resolution[1] > camera.source_resolution[1]:
                y = camera.source_resolution[1] - camera.camera_resolution[1]

            return pygame.Rect((x, y), camera.camera_resolution)

We now have a complete CameraBehavior that puts the focal rectangle
in the top left of the screen without going outside the bounds of the
source surface!

