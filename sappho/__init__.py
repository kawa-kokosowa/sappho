if __name__ == "__main__":
    __version__ = "0.5.0"
else:
    from animatedsprite import AnimatedSprite
    from tilemap import TileMap, Tilesheet, tmx_file_to_tilemaps
    from layers import SurfaceLayers
    from camera import (Camera, CameraBehavior,
                        CameraCenterBehavior, CameraOutOfBounds)
