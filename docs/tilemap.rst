Tilesheets and tilemaps
=======================

.. py:module:: sappho.tilemap

Tile
----

The Tile class is the base for all tilesheets. It represents a single
tile on the map, and contains the tile's flags, such as whether the tile
is solid (ie, can't be walked through).

.. autoclass:: Tile

Tilesheet
---------

A tilesheet is a collection of tiles, usually loaded from a tilesheet
image. A tilesheet image looks like this:

.. image:: /images/tilesheet.png

A tilesheet is represented in Sappho by the :py:class:`Tilesheet` class.
It holds information about the size of the tiles on the tilesheet,
a reference to each tile, and of course, the :py:class:`pygame.Surface`
that holds the tilesheet itself.

.. autoclass:: Tilesheet
   :members: parse_rules, from_file
