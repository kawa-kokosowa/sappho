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

TileMap
-------

The :py:class:`TileMap` class represents the ordered collection of
tiles that make up a game map. Typically, you won't create a TileMap
instance yourself, instead you would load the TileMap from a TMX file
using :py:meth:`tmx_file_to_tilemaps`, which creates a TileMap for each
layer of the TMX map that is passed to it.

.. automethod:: sappho.tilemap.tmx_file_to_tilemaps

Once the TileMap has been created, there are a number of methods available
on it that are useful, such as getting the solid blocks in the map, and
rendering it to a surface.

.. autoclass:: TileMap
   :members: get_solid_blocks, to_surface
