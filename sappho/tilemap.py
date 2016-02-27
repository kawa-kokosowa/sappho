import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, pygame_subsurface):
        super(Tile, self).__init__()
        self.image = pygame_subsurface


class Tile(object):

    def __init__(self, id_, surface, subsurface):
        self.id_ = id_
        self.surface = surface
        self.subsurface = subsurface


class Tilesheet(object):

    def __init__(self, surface, tiles, tile_size):
        self.surface = surface
        self.tiles = tiles
        self.tile_size = tile_size


    @classmethod
    def from_file(cls, file_path, tile_width, tile_height):
        tilesheet_surface = pygame.image.load(file_path)

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
            tile = Tile(id_=tile_id,
                        surface=tilesheet_surface,
                        subsurface=subsurface)
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


class TileMap(object):

    def __init__(self, tilesheet, tiles):
        """

        Arguments:
            tilesheet
            tiles (list[Tile]): --

        """

        self.tilesheet = tilesheet
        self.tiles = tiles

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
                new_surface.blit(tile.subsurface, tile_position)

        return new_surface

    @classmethod
    def from_csv_string_and_tilesheet(cls, csv_string, tilesheet):
        sheet = []

        for line in csv_string.split('\n'):
            row = []

            for tile_id_string in line.split(','):

                if not tile_id_string:

                    continue

                tile_id = int(tile_id_string)
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
