if __name__ == "__main__":
    __version__ = "0.1"
else:
    from animatedsprite import AnimatedSprite
    from tilemap import TileMap, Tilesheet
    from tmx import tmx_file_to_tilemap_csv_string
    from layers import SurfaceLayers
