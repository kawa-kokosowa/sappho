"""Honestly most useful for animatedsprite,
contextsprite, etc.

"""

import pygame


class CollisionSprite(pygame.sprite.Sprite):
    """A sprite with a position and collision data.

    Especially useful for sprites whose state changes
    a lot, notably through its update_state() method,
    affecting its mask, rect.

    Attributes:
        sprite (pygame.Sprite): The sprite which represents
            this actor, and from which the actor's mask and
            rect are derived every call to update_state().
        rect (pygame.Rect): Rectangle whose dimensions
            are updated (update_state) to reflect that
            of the sprite's rect dimensions. Absolute position
            of the Actor is set by setting this rect's:
            topleft, center, etc.
        mask (pygame.Mask): Reference to sprite's mask,
            which is updated every update_state().

    """

    def __init__(self, sprite):
        """Create a CollisionSprite, using data from the
        supplied sprite.

        Arguments:
            sprite (pygame.Sprite): A Pygame sprite with the
                special attribute of mask and special method
                of update_state(). QUACK!

        """

        super(CollisionSprite, self).__init__()

        self.sprite = sprite
        self.rect = self.sprite.rect
        self.mask = self.sprite.mask

    def update_state(self, timedelta):
        """Set the rect and mask attributes after updating
        the sprite's state.

        Arguments:
            timedelta (int): Typically the clock timedelta
                resulting from the game's clock.get_time().

        """

        self.sprite.update_state(timedelta)
        self.rect.size = self.sprite.size
        self.mask = self.sprite.mask

    def collides_with_any_in_group(self, pygame_sprite_group):
        """Return True if this CollisionSprite collides with
        any of the sprites in the provided sprite group.

        Collisions are checked by first getting all the sprites
        from the pygame_sprite_group which collide with this
        CollisionSprite based on rectangles. Using those sprites
        gotten, see if any collide based on mask.

        Returns:
            bool: True if colliding based on mask.

        """

        # shorthand
        spritecollide = pygame.sprite.spritecollide
        collide_mask = pygame.sprite.collide_mask

        # get the tiles (sprites) colliding with this
        # collision sprite based on rect property.
        tiles_colliding_by_rect = (spritecollide(self,
                                                 pygame_sprite_group,
                                                 False,
                                                 collided=(pygame.sprite
                                                           .collide_rect)))

        # of the tiles which intersected based on rect, see if any tiles
        # collide with this CollisionSprite based on mask
        for tile_whose_rect_collides in tiles_colliding_by_rect:

            if collide_mask(tile_whose_rect_collides, self) is not None:
                return True

        return False
