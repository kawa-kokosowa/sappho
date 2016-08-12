"""Handle generic pygame collision.

The ColliderSprite lets you have a positional
sprite, with a mask and rect, which can be
efficiently and easily tested against sprite
groups with similar data.

"""

import pygame


class Collision(Exception):

    def __init__(self, collision_details):
        self.collision_details = collision_details


class ColliderSprite(pygame.sprite.Sprite):
    """A sprite with a position and collision data.

    Especially useful for sprites whose state changes
    a lot, notably through its update_state() method,
    affecting its mask, rect.

    The update() method will update the sprite as well, there's
    no reason for you to access said sprite anymore.

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
        """Create a ColliderSprite, using data from the
        supplied sprite.

        Arguments:
            sprite (pygame.Sprite): A Pygame sprite with the
                special attribute of mask and special method
                of update_state(). QUACK!

        """

        super(ColliderSprite, self).__init__()

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

    def collides_rect(self, sprite_group):
        return pygame.sprite.spritecollide(self, sprite_group, False,
                                           collided=pygame.sprite.collide_rect)

    def collides_rect_mask(self, sprite_group):

        for sprite_whose_rect_collides in self.collides_rect(sprite_group):

            if (hasattr(self, 'mask')
                    and hasattr(sprite_whose_rect_collides, 'mask')
                    and (pygame.sprite
                         .collide_mask(sprite_whose_rect_collides, self))):

                print("mask collision")
                return sprite_whose_rect_collides

            elif (not hasattr(self, 'mask')) and (not hasattr(self, 'mask')):
                print("rect collision")
                return sprite_whose_rect_collides

        else:
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

        if self.collides_rect_mask(sprite_group):
            self.rect.topleft = old_topleft
            raise Collision("some side...")

    # TODO: what if I want diagonal!?
    def sprites_in_path(self, new_coord, sprite_group):
        """Return the sprites this ColliderSprite would "run through"
        and thus collide with if it moved to new_coord.

        Warning:
            This does not work diagonally! This is shamefully bad, but
            works perfectly for orthogonal movement.

        """

        current_rect = self.rect
        future_rect = self.rect.copy()
        future_rect.topleft = new_coord
        collision_rect = future_rect.union(current_rect)
        self.rect = collision_rect
        colliding_with = self.collides_rect(sprite_group)
        self.rect = current_rect
        return colliding_with
