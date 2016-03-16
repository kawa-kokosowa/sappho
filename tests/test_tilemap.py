import os
import textwrap

import pygame

from .. import sappho
from ..sappho.tilemap import Tile


class TestTile(object):
    def test_tile_instantiation(self):
        surface = pygame.surface.Surface((1, 1))
        tile = Tile(0, surface)

        assert(tile.id_ == 0)
        assert(tile.solid_block == False) # default is False so check that


class TestTilesheet(object):
    def test_from_file(self):
        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "tilesheet.png"))

        tilesheet = sappho.Tilesheet.from_file(path, 1, 1)

        # Test that tile rules are loaded correctly
        assert(tilesheet.tiles[0].solid_block == True)

    def test_subsurface(self):
        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "tilesheet.png"))

        tilesheet = sappho.Tilesheet.from_file(path, 1, 1)

        # Grab the tile at (0, 0) and blit it's subsurface to another surface,
        # then compare it against a master surface to ensure it's the color we
        # want

        target_surface = pygame.surface.Surface((1, 1))
        target_surface.blit(tilesheet.tiles[0].image, (0, 0))

        master_surface = pygame.surface.Surface((1, 1))
        master_surface.fill((255, 0, 0))

        target_view = target_surface.get_view().raw
        master_view = master_surface.get_view().raw
        
        assert(target_view == master_view)


class TestTilemap(object):
    TILEMAP_CSV = """\
    0,1,2
    5,4,3
    """
    
    def setup(self):
        # Load a tilesheet to use for our tilemap

        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "tilesheet.png"))

        self.tilesheet = sappho.Tilesheet.from_file(path, 1, 1)

    def test_from_csv(self):
        csv = textwrap.dedent(self.TILEMAP_CSV)
        tilemap = sappho.TileMap.from_csv_string_and_tilesheet(csv,
                                                               self.tilesheet)

        # The tile ID 0 is set as a solid block, and this is at (0, 0) to (1, 1)
        # in the tilemap. Here, we check that a solid block has been correctly
        # entered into the tilemap.
        assert(len(tilemap.solid_blocks) == 1)
        assert(tilemap.solid_blocks[0].topleft == (0, 0)) 
        assert(tilemap.solid_blocks[0].bottomright == (1, 1))
