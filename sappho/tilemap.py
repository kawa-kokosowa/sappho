import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, id_, image, solid_block=False):
        super(Tile, self).__init__()
        self.id_ = id_
        self.image = image
        self.solid_block = solid_block


class Tilesheet(object):

    def __init__(self, surface, tiles, tile_size):
        self.surface = surface
        self.tiles = tiles
        self.tile_size = tile_size

    @staticmethod
    def parse_rules(path_to_rules_file):
        
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


# NOTE: could become TileMapLayer
class TileMap(object):

    def __init__(self, tilesheet, tiles, solid_blocks=[]):
        """

        Arguments:
            tilesheet
            tiles (list[Tile]): --

        """

        self.tilesheet = tilesheet
        self.tiles = tiles
        self.solid_blocks = solid_blocks

    def to_surface(self):
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
    def from_csv_string_and_tilesheet(cls, csv_string, tilesheet):
        sheet = []
        solid_blocks = []

        for y, line in enumerate(csv_string.split('\n')):
            row = []

            for x, tile_id_string in enumerate(line.split(',')):

                if not tile_id_string:

                    continue

                tile_id = int(tile_id_string)
                tile = tilesheet.tiles[tile_id]

                if tile.solid_block:
                    left_top = (x * tilesheet.tile_size[0],
                                y * tilesheet.tile_size[1])
                    block = pygame.rect.Rect(left_top, tilesheet.tile_size)
                    solid_blocks.append(block)

                # create absolute rect and add to group

                row.append(tile)

            sheet.append(row)

        return cls(tilesheet, sheet, solid_blocks)


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
