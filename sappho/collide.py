"""Handle generic pygame collision.

The ColliderSprite lets you have a positional
sprite, with a mask and rect, which can be
efficiently and easily tested against sprite
groups with similar data.

"""

import pygame


# TODO: this is pretty unnecessary now...
def collides_rect(sprite, sprite_group):
    """

    Boilerplate for checking rectangular collision of provided
    sprite against sprites in the provided sprite_group.

    """

    return pygame.sprite.spritecollide(sprite, sprite_group, False)


def collides_rect_mask(sprite, sprite_group):
    """See if provided sprite collides with any in the sprite_group
    by rect first, then check by mask if exists.

    Arguments:
        sprite (pygame.Sprite): ...
        sprite_group (pygame.sprite.Group): See if this ColliderSprite
            collides with any sprites in `sprite_group`.

    Returns:
        None: If there are no collisions.
        pygame.sprite.Sprite: the first sprite to collide with
            this ColliderSprite based on rect and possibly also
            mask (if exists on both this ColliderSprite and the
            other sprite being checked!).

    """

    for sprite_whose_rect_collides in collides_rect(sprite, sprite_group):

        if (hasattr(sprite, 'mask')
                and hasattr(sprite_whose_rect_collides, 'mask')
                and (pygame.sprite
                     .collide_mask(sprite_whose_rect_collides, sprite))):

            return sprite_whose_rect_collides

        elif (not hasattr(sprite, 'mask')) and (not hasattr(sprite, 'mask')):
            return sprite_whose_rect_collides

    return None


def move_as_close_as_possible(sprite, destination, sprite_group):
    """Move along a line to destination coordinate, stopping before
    potential collision.

    Move as close as possible to `destination` without collision.

    Warning:
        This isn't fast! It lacks any decent heuristics, such as
        line-based collisions. I'll be benchmarking this method
        against line-based collision heuristics in the future.

    Arguments:
        sprite (pygame.Sprite): the sprite to move as close...
        destination (tuple[x, y]): The goal coordinate to move to, or
            at least as close to as possible before colliding.
        sprite_group (pygame.sprite.Group): Pygame sprite group, whose
            sprites are check each time we move one pixel
            toward the destination.

    Returns:
        pygame.Sprite: The first sprite detected which prevented
            moving further in the path.
        None: Moved to destination without collision.

    """

    # Figure out the x and y increments!
    #
    # I use "increment" herein to mean "step which approaches,
    # by one, the destination.
    #
    # For both the x and y axis, get the "step"
    # (increment or decrement) which will
    # eventually bring us to the goal.
    goal_x, goal_y = destination

    if goal_x > sprite.rect.left:
        x_increment = 1
    elif goal_x < sprite.rect.left:
        x_increment = -1
    else:
        x_increment = 0

    if goal_y > sprite.rect.top:
        y_increment = 1
    elif goal_y < sprite.rect.top:
        y_increment = -1
    else:
        y_increment = 0

    # This loop will return the first sprite it finds to collide,
    # or we'll return None (later) if it can't find anything!
    while sprite.rect.topleft != (goal_x, goal_y):
        # last_safe_topleft allows us to reset to the last known
        # good/noncolliding coordinate in the event of a collision
        last_safe_topleft = sprite.rect.topleft

        # If y is already at its goal, there's no need to increment
        if sprite.rect.top != goal_y:
            sprite.rect.top += y_increment

        # ... same thing for x and its goal.
        if sprite.rect.left != goal_x:
            sprite.rect.left += x_increment

        colliding_with = collides_rect_mask(sprite, sprite_group)

        if colliding_with:
            sprite.rect.topleft = last_safe_topleft
            return colliding_with

    return None


def sprites_in_orthogonal_path(sprite, new_coord, sprite_group):
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

    current_rect = sprite.rect
    future_rect = sprite.rect.copy()
    future_rect.topleft = new_coord
    collision_rect = future_rect.union(current_rect)
    sprite.rect = collision_rect
    colliding_with = collides_rect(sprite, sprite_group)
    sprite.rect = current_rect
    return colliding_with


def collides_line(sprite, line_point_a, line_point_b, sprite_group):
    """Efficiently check if any sprites along a line collide,
    return True on first result, False if no collision.

    Arguments:
        line_point_a (tuple[int, int]): --

    """

    pass


def lines_intersection(line_a, line_b):
    """Return the point in which lines intersect, else
    return None.

    Arguments:
        line_a (tuple[int, int]): --

    http://webcache.googleusercontent.com/search?q=cache:Ur-EPX41x00J:devmag.org.za/2009/04/17/basic-collision-detection-in-2d-part-2/+&cd=1&hl=en&ct=clnk&gl=us&client=ubuntu

    """

    pass
