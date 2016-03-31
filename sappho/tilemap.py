"""Tile engine; tile map, tilesheet system.

Has impassability support.

"""

import pygame

import xml.etree.ElementTree as ET


class Tile(pygame.sprite.Sprite):
    """A tile object is a sprite, which is typically
    a subsurface of a tilesheet.

    Attributes:
        id_ (str): The ID of this tile in its respective
            tilesheet.
        image (pygame.surface.Surface):
        solid_block (bool): If true, this entire tile
            is completely impassible.

    """

    def __init__(self, id_, image, solid_block=False):
        super(Tile, self).__init__()
        self.id_ = id_
        self.image = image
        self.solid_block = solid_block


class Tilesheet(object):
    """Efficient place to  update, subsurface tile
    graphics.

    Attributes:
        surface (pygame.surface.Surface):
        tiles (list[Tile]): The tiles composing this
            Tilesheet.
        tile_size (tuple[int, int]): The size of each
            tile in pixels (x, y).

    """

    def __init__(self, surface, tiles, tile_size):
        self.surface = surface
        self.tiles = tiles
        self.tile_size = tile_size

    @staticmethod
    def parse_rules(path_to_rules_file):
        """Get properties for tile IDs from the
        path_to_rules_file.

        Argument:
            path_to_rules_file (str):

        Returns:
            str:

        """
        
        with open(path_to_rules_file) as f:
            rules = f.readlines()

        tile_rules = {}

        for rule in rules:
            tile_ids_affected, flags = rule.split('=')
            tile_ids_affected = [id_ for id_ in tile_ids_affected.split(',')]
            flags = [flag.strip() for flag in flags.split(',')]

            for tile_id in tile_ids_affected:
                
                if '-' in tile_id:
                    first_id, last_id = tile_id.split('-')
                    first_id = int(first_id)
                    last_id = int(last_id)

                    for tile_id in xrange(first_id, last_id + 1):
                        tile_rules[int(tile_id)] = flags

                tile_rules[int(tile_id)] = flags

        return tile_rules

    @classmethod
    def from_file(cls, file_path, tile_width, tile_height):
        """Creates a tilesheet, and its tiles, from a
        file, as well as tile width and height specification.

        Arguments:
            file_path (str):
            tile_width (int):
            tile_height(int):

        """

        tilesheet_surface = pygame.image.load(file_path)
        tile_rules = cls.parse_rules(file_path + ".rules")

        tile_size = (tile_width, tile_height)
        tilesheet_width, tilesheet_height = tilesheet_surface.get_size()
        tilesheet_width_in_tiles = tilesheet_width // tile_width
        tilesheet_height_in_tiles = tilesheet_height // tile_height
        total_tiles = tilesheet_width_in_tiles * tilesheet_height_in_tiles

        # tile initialization; buid all the tiles
        tiles = []

        for tile_id in range(total_tiles):
            subsurface = cls.tile_subsurface_from_tile_id(tilesheet_surface,
                                                          tile_size,
                                                          tile_id)

            solid = tile_id in tile_rules and 'solid_block' in tile_rules[tile_id]
            tile = Tile(id_=tile_id,
                        image=subsurface,
                        solid_block=solid)
            tiles.append(tile)

        return Tilesheet(tilesheet_surface, tiles, tile_size)

    @staticmethod
    def tile_subsurface_from_tile_id(tilesheet_surface, tile_size, tile_id):
        """Create a subsurface for a tile from the tilesheet surface.

        Arguments:
            tilesheet_surface (pygame.surface.Surface):
            tile_size (list[int, int]): (x, y) pixel dimensions
                of all tiles.
            tile_id (int): The tile ID to graph the graphic from
                the tilesheet surface for.

        Return:
            pygame.surface.Surface:

        """

        tilesheet_width_in_tiles = (tilesheet_surface.get_size()[0] /
                                    tile_size[0])
        top_left_in_tiles = index_to_coord(tilesheet_width_in_tiles,
                                           tile_id)
        subsurface_top_left = (top_left_in_tiles[0] * tile_size[0],
                               top_left_in_tiles[1] * tile_size[1])
        position_rect = pygame.Rect(subsurface_top_left, tile_size)
        area_on_tilesheet = position_rect
        subsurface = tilesheet_surface.subsurface(position_rect)

        return subsurface


class TileMap(object):
    """A 2D grid arrangement of tiles, accompanied by
    passability information.

    Notes:
        You can use this as a layer for a map.
        Can be used as a tile map layer!

        You could use a tilemap per "layer" and then
        move through the layers of TileMap objects
        respectively, so when you move up stairs
        you're affected by solids of that same
        layer/level/TileMap object.

        This is to stress that a 3D tilemap is not
        only not needed, but a bad idea!

    """

    def __init__(self, tilesheet, tiles):
        """

        Arguments:
            tilesheet
            tiles (list[Tile]): --

        """

        self.tilesheet = tilesheet
        self.tiles = tiles

    def get_solid_blocks(self):
        """Return the Pygame rect of all
        the tiles which have the solid_block
        attribute.

        Returns:
            list(pygame.Rect): --

        """

        solid_blocks = []

        for y, row_of_tiles in enumerate(self.tiles):

            for x, tile in enumerate(row_of_tiles):
                
                if tile.solid_block:
                    left_top = (x * self.tilesheet.tile_size[0],
                                y * self.tilesheet.tile_size[1])
                    block = pygame.rect.Rect(left_top,
                                             self.tilesheet.tile_size)
                    solid_blocks.append(block)

        return solid_blocks

    def to_surface(self):
        """Blit the tiles to a surface and return it!

        Returns:
            pygame.surface.Surface: --

        """

        tile_size_x, tile_size_y = self.tilesheet.tile_size

        width_in_tiles = len(self.tiles[0])
        height_in_tiles = len(self.tiles)

        layer_size = (width_in_tiles * tile_size_x,
                      height_in_tiles * tile_size_y)

        new_surface = pygame.Surface(layer_size, pygame.SRCALPHA, 32)
        new_surface.fill([0, 0, 0, 0])

        for y, row_of_tiles in enumerate(self.tiles):

            for x, tile in enumerate(row_of_tiles):
                # blit tile subsurface onto respective layer
                tile_position = (x * tile_size_x, y * tile_size_y)
                new_surface.blit(tile.image, tile_position)

        return new_surface

    @classmethod
    def from_csv_string_and_tilesheet(cls, csv_string, tilesheet, firstgid=0):
        """Create a tilemap using a CSV of tile IDs and
        a tilesheet.

        Arguments:
            csv_string (str):
            tilesheet (Tilesheet):
            firstgid (int): ID of the first tile

        """

        sheet = []

        for y, line in enumerate(csv_string.split('\n')):
            row = []

            for x, tile_id_string in enumerate(line.split(',')):

                if not tile_id_string:

                    continue

                tile_id = int(tile_id_string) - firstgid
                tile = tilesheet.tiles[tile_id]
                row.append(tile)

            sheet.append(row)

        return cls(tilesheet, sheet)


def index_to_coord(width, i):
    """Return the 2D position (x, y) which corresponds to 1D index.

    Examples:
      If we have a 2D grid like this:

      0 1 2
      3 4 5
      6 7 8

      We can assert that element 8 is of the coordinate (2, 2):
      >>> (2, 2) == index_to_coord(3, 8)
      True

    """

    if i == 0:

        return (0, 0)

    else:

        return ((i % width), (i // width))


def tmx_file_to_tilemaps(tmx_file_path, tilesheet):
    """Read TMX file from path and return
    a list of TileMaps (one TileMap per layer).

    Arguments:
        tmx_file_path (str)
        tilesheet (Tilesheet)

    Returns:
        list[TileMap]: Each layer gets its own TileMap!

    Note:
        Uses CSV layers; TMX allows all kinds, but
        CSV is the default.

    """

    tree = ET.parse(tmx_file_path)
    root = tree.getroot()  # <map ...>

    firstgid = int(root.findall(".//tileset")[0].attrib["firstgid"])

    csv_layers = []

    for layer_data in root.findall(".//layer/data"):
        data_encoding = layer_data.attrib['encoding']

        if data_encoding != 'csv':

            raise TMXLayersNotCSV(data_encoding)

        layer_csv = layer_data.text.strip()
        csv_layers.append(layer_csv)

    tilemaps = []

    for layer in csv_layers:
        layer_tilemap = TileMap.from_csv_string_and_tilesheet(layer,
                                                              tilesheet,
                                                              firstgid)

        tilemaps.append(layer_tilemap)

    return tilemaps
