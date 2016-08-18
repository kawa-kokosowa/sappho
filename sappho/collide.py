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
    a lot, notably through its update() method,
    affecting its mask, rect.

    The update() method will update the sprite as well, there's
    no reason for you to access said sprite anymore.

    Attributes:
        sprite (pygame.Sprite): The sprite which represents
            this actor, and from which the actor's mask and
            rect are derived every call to update().
        rect (pygame.Rect): Rectangle whose dimensions
            are updated (update) to reflect that
            of the sprite's rect dimensions. Absolute position
            of the Actor is set by setting this rect's:
            topleft, center, etc.
        mask (pygame.Mask): Reference to sprite's mask,
            which is updated every update().

    """

    def __init__(self, sprite):
        """Create a ColliderSprite, using data from the
        supplied sprite.

        Arguments:
            sprite (pygame.Sprite): A Pygame sprite with the
                special attribute of mask and special method
                of update(). QUACK!

        """

        super(ColliderSprite, self).__init__()

        self.sprite = sprite
        self.rect = self.sprite.rect

        if hasattr(sprite, 'mask'):
            self.mask = self.sprite.mask

    def update(self, timedelta):
        """Set the rect and mask attributes after updating
        the sprite's state.

        Arguments:
            timedelta (int): Typically the clock timedelta
                resulting from the game's clock.get_time().

        """

        self.sprite.update(timedelta)
        self.rect.size = self.sprite.rect.size

        if hasattr(self, 'mask'):
            self.mask = self.sprite.mask

    def collides_rect(self, sprite_group):
        return pygame.sprite.spritecollide(self, sprite_group, False,
                                           collided=pygame.sprite.collide_rect)

    def collides_rect_mask(self, sprite_group):
        """See if collides by rect first, then check by mask if exists.

        Arguments:
            sprite_group (pygame.sprite.Group): See if this ColliderSprite
                collides with any sprites in `sprite_group`.

        Returns:
            None: If there are no collisions.
            pygame.sprite.Sprite: the first sprite to collide with
                this ColliderSprite based on rect and possibly also
                mask (if exists on both this ColliderSprite and the
                other sprite being checked!).

        """

        for sprite_whose_rect_collides in self.collides_rect(sprite_group):

            if (hasattr(self, 'mask')
                    and hasattr(sprite_whose_rect_collides, 'mask')
                    and (pygame.sprite
                         .collide_mask(sprite_whose_rect_collides, self))):

                return sprite_whose_rect_collides

            elif (not hasattr(self, 'mask')) and (not hasattr(self, 'mask')):
                return sprite_whose_rect_collides

        else:
            return None

    # TODO:
    # could be called something like rect_mask_path and iterate
    # through up to the collision point returning that value.
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

    # TODO, FIXME
    def move_as_close_as_possible(self, destination, sprite_group):
        """Move as close as possible to `destination` without collision.

        """

        goal_x, goal_y = destination
        current_x, current_y = self.rect.topleft

        # FIRST: figure out the x and y increments
        #
        # For both the x and y axis, get the "step"
        # (increment or decrement) which will
        # eventually bring us to the goal.
        if goal_x > self.rect.left:
            x_increment = 1
        elif goal_x < self.rect.left:
            x_increment = -1
        else:
            x_increment = 0

        if goal_y > self.rect.top:
            y_increment = 1
        elif goal_y < self.rect.top:
            y_increment = -1
        else:
            y_increment = 0

        # Ye dangerous infinite loop: exits when either a collision
        # is detected, or we have arrived at the goal/destination.
        while True:
            # last_safe_topleft allows us to reset to the last known
            # good/noncolliding coordinate in the event of a collision
            last_safe_topleft = self.rect.topleft

            # If y is already at its goal, there's no need to increment
            if not self.rect.top == goal_y:
                self.rect.top += y_increment

            # ... same thing for x and its goal.
            if not self.rect.left == goal_x:
                self.rect.left += x_increment

            colliding_with = self.collides_rect_mask(sprite_group)

            if colliding_with:
                self.rect.topleft = last_safe_topleft
                return colliding_with
            elif self.rect.topleft == (goal_x, goal_y):
                # we're at our goal, we've not encountered
                # a collision.
                return None

    # TODO: what if I want diagonal!?
    def sprites_in_path(self, new_coord, sprite_group):
        """Return the sprites this ColliderSprite would "run through"
        and thus collide with if it moved to new_coord.

        Warning:
            This does not work diagonally! This is shamefully bad, but
            works perfectly for orthogonal movement.

        Arguments:
            new_coord (tuple[int, int]): topleft coordinate value this
                ColliderSprite would hypotherically have at the end of
                this path.
            sprite_group (pygame.sprite.Group): ...

        """

        current_rect = self.rect
        future_rect = self.rect.copy()
        future_rect.topleft = new_coord
        collision_rect = future_rect.union(current_rect)
        self.rect = collision_rect
        colliding_with = self.collides_rect(sprite_group)
        self.rect = current_rect
        return colliding_with
