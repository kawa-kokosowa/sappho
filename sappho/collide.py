"""Handle generic pygame collision.

Maybe this shouldn't ever move a sprite, but always return
a coordinate and any sprites it collides with.

"""

import pygame


# TODO: this is pretty unnecessary now...
def collides_rect(sprite, sprite_group):
    """

    Boilerplate for checking rectangular collision of provided
    sprite against sprites in the provided sprite_group.

    """

    return pygame.sprite.spritecollide(sprite, sprite_group, False)


def add_rect_mask_if_missing_mask(sprite):
    """So you can do rect/mask collisions.

    """

    if not hasattr(sprite, 'mask'):
        new_mask = pygame.mask.Mask(sprite.rect.size)
        new_mask.fill()
        sprite.mask = new_mask


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

    add_rect_mask_if_missing_mask(sprite)

    for sprite_whose_rect_collides in collides_rect(sprite, sprite_group):
        add_rect_mask_if_missing_mask(sprite_whose_rect_collides)

        if pygame.sprite.collide_mask(sprite_whose_rect_collides, sprite):
            return sprite_whose_rect_collides

    return None


def move_as_close_as_possible(sprite, destination, sprite_group):
    """Return how close sprite can go to destination without collision,
    along with the first sprite blocking its progress (if any).

    "Position" herein will always refer to a position
    for sprite.rect.topleft.

    Say you have a SPACESHIP (S), "blank space" (-), the
    destination (D), and a collidable BLOCK (B). If the
    SPACESHIP moves at a velocity of x+5 y+5, this function
    would would take (6, 6) as the `destination`, and it would
    return ((3, 3), <sprite of the BLOCK>). This directly
    mitigates "bad" collision where you could simply jump from
    1,1 to 6,6 despite there being a collision in the path (BLOCK).

        123456
      1 S-----
      2 ------
      3 ------
      4 ---B--
      5 ------
      6 -----D

    In the example above, if there were no BLOCK (B) the return value
    would be ((6,6), None).

    Warning:
        This isn't fast! It lacks any decent heuristics, such as
        line-based collisions. I'll be benchmarking this method
        against line-based collision heuristics in the future.

    Arguments:
        sprite (pygame.Sprite): This sprite is used to incrementally
            move toward the destination, continuously checking
            if colliding with any in sprite_group. The sprite's position
            will not be affected (you will have to update the
            sprite.rect.topleft respectively, yourself).
        destination (tuple[x, y]): The goal coordinate to move to, or
            at least as close to as possible before colliding.
        sprite_group (pygame.sprite.Group): Pygame sprite group, whose
            sprites are check each time we move one pixel
            toward the destination.

    Returns:
        tuple: The first element is the "topleft" coordinate
            representing the closest sprite may move toward the
            destination before a collision occurs. The first element
            coordinate will be one of the following:
              * At the original "topleft" position of sprite, i.e.,
                sprite.rect.topleft
              * The destination provided: if there were no collisions
                moving between original position and destination.
              * In between original and destination positions: when
                there was a collision, this will be the last value
                that didn't collide along that path toward destination.
            The second element is the first sprite which
            prevents progressing further toward destination. The second
            element could be None if sprite can move to destination
            without any collisions from sprite_group.

    """

    original_position = sprite.rect.topleft

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
            sprite.rect.topleft = original_position
            return (last_safe_topleft, colliding_with)

    return (destination, None)


def sprites_in_orthogonal_path(sprite, new_coord, sprite_group):
    """Return the sprites this ColliderSprite would "run through"
    and thus collide with if it moved to new_coord.

    Warning:
        This does not work diagonally! This is only good for
        quickly checking collisions along an orthogonal path.

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
