SurfaceLayers
=============

.. py:module:: sappho.layers

In a game, you'll typically want to have multiple layers of drawable
objects - for example, one for the background, one for collidable
objects, one for the character, and one for your overlay, or HUD.
The SurfaceLayers class provides a way to keep these layers in order,
and render them correctly.

.. autoclass:: SurfaceLayers
   :members: create_surface_layers, render

Typical usage
-------------

Typically, you will want two :py:class:`SurfaceLayers` objects, one for
the game's map (which would ideally be rendering to a 
:py:class:`Camera <sappho.camera.Camera>`), and one for the game as a
whole, containing the aforementioned Camera, and your game elements,
such as a heads up display. This setup would look something like this::

    # Screen resolution.
    RESOLUTION = (800, 600)

    # Map camera and layers
    map_surfaces = [...]
    map_camera = sappho.camera.Camera(map_surfaces[0].get_size(),
                                      RESOLUTION, # Screen resolution
                                      (100, 100)) # Size of the view
    map_layers = sappho.layers.SurfaceLayers(map_camera.source_surface,
                                             len(map_surfaces))

    # Heads up display (created with RESOLUTION as to fill the whole screen)
    hud = pygame.Surface(RESOLUTION)

    # Overall game layers.
    # 2 layers - one for the map camera, one for the HUD
    game_layers = sappho.layers.SurfaceLayers(screen, 2)

    while game_is_running:
        # Any code that needs to be run before screen updates can go here,
        # for example, updating the HUD
        ...

        # Render the map surfaces to the map SurfaceLayers object
        for i, surface in enumerate(map_surfaces):
            map_layers[i].blit(surface, (0, 0))

        # Render the map_layers to the camera then update the camera
        map_layers.render()
        map_camera.update()

        # Render the map camera and the HUD to game_layers
        game_layers[0].blit(map_camera, (0, 0))
        game_layers[1].blit(hud, (0, 0))

        # Render everything to the screen and update it with our changes
        game_layers.render()
        pygame.display.flip()

