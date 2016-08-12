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

        if hasattr(sprite, 'mask'):
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

        if hasattr(self, 'mask'):
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

            if (hasattr(self, 'mask')
                    and hasattr(tile_whose_rect_collides, 'mask')
                    and (collide_mask(tile_whose_rect_collides, self))):

                print("mask collision")
                return tile_whose_rect_collides

            elif (not hasattr(self, 'mask')) and (not hasattr(self, 'mask')):
                print("rect collision")
                return tile_whose_rect_collides

        return None

    # TODO: test all proceeding coordinates, returning first obstruction?
    def try_to_move(self, new_coord, sprite_group):
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
        self.rect.topleft = new_coord

        if self.collides_with_any_in_group(sprite_group):
            self.rect.topleft = old_topleft
            raise Collision("some side...")

    # TODO: what if I want diagonal!?
    def sprites_in_path(self, new_coord, sprite_group):
        """Test every position up to new_coord.

        Warning: this only works for orthoganal shooting, i.e.,
        up, down, left, right.

        """

        current_rect = self.rect
        future_rect = self.rect.copy()
        future_rect.topleft = new_coord
        collision_rect = future_rect.union(current_rect)
        self.rect = collision_rect
        colliding_with = self.collides_with_any_in_group(sprite_group)
        self.rect = current_rect
        return colliding_with

    def try_to_movable_coordinate_preceeding(self):
        pass
