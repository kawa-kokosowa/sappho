"""Handle generic pygame collision.

The CollisionSprite lets you have a positional
sprite, with a mask and rect, which can be
efficiently and easily tested against sprite
groups with similar data.

"""

import pygame


class Collision(Exception):

    def __init__(self, collision_details):
        self.collision_details = collision_details


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

        Arguments:
            pygame_sprite_group (pygame.sprite.Group): ...

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

    def try_to_move(self, x_speed, y_speed, sprite_group):
        """Try to move to a position and either succeed
        or raise a Collision exception.

        Will not change position if Collision raised.

        Arguments:
            x_speed (int): this number will be added to the
                rectangle's topleft x!
            y_speed (int): this number will be added to the
                rectangle's topleft y!
            sprite_group (pygame.sprite.Group): ...

        Raises:
            Collision: ...

        """

        old_topleft = self.rect.topleft
        potential_x_coord = old_topleft[0] + x_speed
        potential_y_coord = old_topleft[1] + y_speed
        self.rect.topleft = (potential_x_coord, potential_y_coord)

        if self.collides_with_any_in_group(sprite_group):
            self.rect.topleft = old_topleft
            raise Collision("some side...")
