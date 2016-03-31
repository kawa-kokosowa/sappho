Animated sprites
================

.. py:module:: sappho.animatedsprite

The `animatedsprite` module contains tools for creating
animated sprites in Pygame, as well as creating "anchored"
animations, which allow you to pin one animation to another,
with frame-by-frame pin-coordinate(s).

AnimatedSprite overview
-----------------------

An `AnimatedSprite` is typically loaded from GIF with
`AnimatedSprite.from_file()`. It provides an abstraction
of each frame, which also provides its :class:`Anchor` data.

.. autoclass:: AnimatedSprite
   :members: from_file
