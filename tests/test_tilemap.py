import os
import textwrap

import pygame

from .. import sappho
from .common import compare_surfaces


class TestTile(object):
    def test_tile_instantiation(self):
        surface = pygame.surface.Surface((1, 1))
        tile = sappho.tilemap.Tile(0, surface)

        assert(tile.id_ == 0)
        assert(len(tile.flags) == 0)
        assert(isinstance(tile.flags, set))


class TestTilesheet(object):
    def test_from_file(self):
        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "tilesheet.png"))

        tilesheet = sappho.tilemap.Tilesheet.from_file(path, 1, 1)

        # Test that tile rules are loaded correctly
        assert(sappho.tilemap.Flags.SOLID in
               tilesheet.tiles[0].flags)

    def test_subsurface(self):
        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "tilesheet.png"))

        tilesheet = sappho.tilemap.Tilesheet.from_file(path, 1, 1)

        # Grab the tile at (0, 0) and blit it's subsurface to another surface,
        # then compare it against a master surface to ensure it's the color we
        # want

        target_surface = pygame.surface.Surface((1, 1))
        target_surface.blit(tilesheet.tiles[0].image, (0, 0))

        master_surface = pygame.surface.Surface((1, 1))
        master_surface.fill((255, 0, 0))

        assert(compare_surfaces(target_surface, master_surface))

    def test_parse_rules(self):
        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "tilesheet.png.rules"))

        rules = sappho.tilemap.Tilesheet.parse_rules(path)

        assert(rules[0] == set([sappho.tilemap.Flags.SOLID]))
        assert(rules[1] == set([sappho.tilemap.Flags.SOLID]))
        assert(rules[2] == set([sappho.tilemap.Flags.SOLID]))
        assert(rules[3] == set([sappho.tilemap.Flags.SOLID]))
        assert(rules[4] == set([sappho.tilemap.Flags.SOLID]))


class TestTilemap(object):
    TILEMAP_CSV = """
    0,1,2
    5,3,4
    """

    def setup(self):
        # Load a tilesheet to use for our tilemap

        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "tilesheet.png"))

        self.tilesheet = sappho.tilemap.Tilesheet.from_file(path, 1, 1)

    def test_from_csv(self):
        csv = textwrap.dedent(self.TILEMAP_CSV).strip()
        tilemap = (sappho.tilemap.TileMap.
                   from_csv_string_and_tilesheet(csv, self.tilesheet))

        # The tile ID 0 is set as a solid block, and this is at (0, 0)
        # to (1, 1) in the tilemap. Here, we check that a solid block
        # has been correctly entered into the tilemap.
        solid_tiles = tilemap.set_solid_toplefts()
        assert(len(solid_tiles) == 5)
        assert(solid_tiles[0].rect.topleft == (0, 0))
        assert(solid_tiles[0].rect.bottomright == (1, 1))

    def test_from_tmx(self):
        testpath = os.path.realpath(__file__)
        path = os.path.abspath(os.path.join(testpath,
                                            "..",
                                            "resources",
                                            "tilemap.tmx"))

        tilemaps = sappho.tilemap.tmx_file_to_tilemaps(path, self.tilesheet)
        tilemap = tilemaps[0]

        # Same as the above test, check for the solid block
        solid_tiles = tilemap.set_solid_toplefts()
        assert(len(solid_tiles) == 5)
        assert(solid_tiles[0].rect.topleft == (0, 0))
        assert(solid_tiles[0].rect.bottomright == (1, 1))

    def test_render(self):
        csv = textwrap.dedent(self.TILEMAP_CSV).strip()
        tilemap = (sappho.tilemap.TileMap.
                   from_csv_string_and_tilesheet(csv, self.tilesheet))

        # Create a surface that has 1x2 strips of red, green, and
        # blue to against the rendered tilemap. This surface has
        # to have the SRCALPHA flag and a depth of 32 to match
        # the surface returned by the render function.
        test_surface = pygame.surface.Surface((3, 2), pygame.SRCALPHA, 32)
        test_surface.fill((255, 0, 0), pygame.Rect(0, 0, 1, 2))
        test_surface.fill((0, 255, 0), pygame.Rect(1, 0, 1, 2))
        test_surface.fill((0, 0, 255), pygame.Rect(2, 0, 1, 2))

        # Render the tilemap
        output_surface = tilemap.to_surface()

        # Compare the two surfaces
        assert(compare_surfaces(test_surface, output_surface))
