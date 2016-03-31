Creating a tilesheet and a map
==============================

In this short tutorial, we'll go over how to create a simple tilesheet,
and use the Tiled editor to create a tilemap. We'll then create a simple
demo game which loads our creations so we can see Sappho in action!

Creating a tilesheet
--------------------

A tilesheet is an image made up of smaller images that represents
a tile. A simple tilesheet, with 10x10 pixel tiles, would look like
this:

.. image:: /images/tilesheet.png

Tiles are indexed from zero in Sappho, and indexing goes right then down.
Let's look at an annotated and enlarged version of the above tilesheet:

.. image:: /images/tilesheet_annotated.png

To start creating a tilesheet, you need to decide on a couple of things:

#. The size of the tiles. All tiles in the tilesheet will share the
   same size, but if you run out of room, you can always make one thing
   span multiple tiles (you'd just have to arrange them right when it
   comes to creating your map)
#. How many tiles you need in your tilesheet. You can always resize it
   later, but it's a good idea to keep the width of the tilesheet the
   same, so you don't throw out your tile indexing (remember, right then
   down). If you resize your tilesheet to add more tiles at the bottom, 
   all the tiles above the resize will keep the same tile ID. 

Let's create a simple 4-tile tilesheet. We'll make each tile 10x10 pixels,
which means we'll have a 20x20 tilesheet image.

Create a new image in your favorite image editing program (for the sake
of the tutorial, we'll use GIMP) and set the size to 20x20 pixels.

