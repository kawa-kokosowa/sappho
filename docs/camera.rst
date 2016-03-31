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

The simplest implementation of a `CameraBehavior` would be to
set the `camera.view_rect.topleft` to the `topleft` of the
`focal_rectangle` within its `move()` method. This effectively sets
the region/area of the `source_surface` used for a subsurface. Said
subsurface is scaled up to the `camera.output_resolution` and then
blit'd to `Camera` itself::

    class TopLeftBehavior(CameraBehavior): 
        def move(self, camera, focal_rectangle):
            camera.view_rect.topleft = focal_rectangle.topleft

Hovever, this does not constrain the view to the bounds of the source
surface, meaning that if the focal rectangle goes off the screen, or
it ventures into an area where the focal rectangle's X or Y position
plus the width of height of the view is greater than the width/height 
of the source surface, an error will occur because you can not create
a subsurface of the source surface that goes outside of the bounds of
the source surface. A :py:exc:`CameraOutOfBounds` exception is raised 
by the :py:func:`Camera.update` function if `camera.view_rect` (as set by
`move()`) is out of bounds. This can be useful in some cases, but
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
            if x + camera.view_rect.width > camera.source_resolution[0]:
                x = camera.source_resolution[0] - camera.view_rect.width
            if y + camera.view_rect.height > camera.source_resolution[1]:
                y = camera.source_resolution[1] - camera.view_rect.height

            camera.view_rect.topleft = (x, y)

We now have a complete CameraBehavior that puts the focal rectangle
in the top left of the screen without going outside the bounds of the
source surface!

