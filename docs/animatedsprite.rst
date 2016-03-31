Animated sprites
================

.. py:module:: sappho.animatedsprite

Tools to create animated sprites in Pygame. This module
also provides a :class:`FrameAnchors` system, so you may
line up two separate animations with
frame-specific-coordinate data.

AnimatedSprite overview
-----------------------

An :class:`AnimatedSprite` is typically loaded from GIF with
:meth:`AnimatedSprite.from_file()`, which loads both
animation and :class:`Anchor` data.

.. automethod:: AnimatedSprite.from_file

So to create an :class:`AnimatedSprite` from a GIF, you'd
do something like this code sample below:

>>> sprite = AnimatedSprite.from_file('somedir/walk.gif')
>>> sprite.image
<Surface(10x10x32 SW)>

The :meth:`AnimatedSprite.from_file()` method will build
the respective :class:`Frame` objects and their
:class:`FrameAnchors`. These frames are sent to the
:class:`AnimatedSprite` constructor, as seen below.

.. automethod:: AnimatedSprite.__init__

Here's what an `AnimatedSprite` looks like:

.. autoclass:: AnimatedSprite

To update the animation, so that it progresses, you need
to pass the :class:`pygame.time.Clock` you
:meth:`pygame.time.Clock.tick()` in your main loop. You
should look at the `demo.py` included from the GitHub repo,
but here's another sample of how you'd use :class:`AnimatedSprite`::

    pygame.init()
    screen = pygame.display.set_mode([700, 500])
    clock = pygame.time.Clock()
    done = False

    while not done:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               done = True 

       screen.blit(animated_sprite.image)
       animated_sprite.update(clock)
       pygame.display.flip()
       clock.tick(60)

    pygame.quit()

Anchoring system
----------------
