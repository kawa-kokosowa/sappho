"""Various functions for detecting pygame sprite collisions!

"""

import doctest

import pygame
import six


class SpatialPartition(object):
    """A pygame.sprite.Group combined with a rectangle, which
    represents its area on the SpatialPartitionGrid to which it
    belongs. This is effectively a cell of the SpatialPartitionGrid.

    You can use self.sprite_group.update and the like! Very useful!

    Attributes:
        rect: pygame.Rect() object, representing the dimensions and
            location on the SpatialPartitionGrid.

    """

    def __init__(self, x, y, width, height):
        """

        Arguments:
            x (int): x-coordinate of topleft.
            y (int): y-coordinate of topleft of this partition.
            width (int): ...
            height (int): ...

        """

        self.rect = pygame.rect.Rect(x, y, width, height)
        self.sprite_group = pygame.sprite.Group()


# TODO/NOTES
# How to keep track which partitions a sprite are in?
# Can use Sprite.groups as a heuristic.
class SpatialPartitionGrid(object):
    """A plane/rectangle divided up into equally-sized,
    non-overlapping "spatial partitions," effectively cells
    of the SpatialPartitionGrid. SpatialPartitionGrids are
    useful for performing actions based on locality, e.g.,
    collisions, updating sprites.

    Specification (spec):
        A SpatialPartitionGrid is created with a 1D list
        of SpatialPartitions whose coordinates and size cover
        the entirety of an implied 2D grid, without overlap.

        All SpatialPartitions are the same size, or
        the ones that differ may be either right-most
        partitions by this much:

          width in pixels - (
            normal partition width in pixels
            * grid width in partitions
          )

        ... or bottom-most partitions differing by this much:

          height in pixels - (
            normal partition height in pixels
            * grid height in partitions
          )

        A bottom-most, right-most partition (the bottom-right corner
        partition) would increase its dimensions according to both
        of the above calculations.

        There are a lot of cases where the "normal partition" would
        be the least common pixel dimensions for a partition. As a
        rule-of-thumb, the unadultrated dimesions, i.e., an "normal
        partition height and width," can always be found at index 0
        of the list.

        The real logic behind this is that you determine your grid width
        first, then you decide how many partitions wide/tall it is, and
        if there's any remainder when you divide the height/width into
        partitions, those remainders go into the bottom-most partitions
        and the right-most partitions.

    See also:
        SpatialPartitionGrid.from_dimensions()

    """

    def __init__(self, list_of_spatial_partitions):
        """

        Arguments:
            list_of_spatial_partitions (list[SpatialPartition]): Ordered
                SpatialPartition list, see: `from_dimensions()`.

        """

        self._partitions = list_of_spatial_partitions
        # we can derive all the meta about our spatial partition grid
        # with very simple calculations.
        self.width = list_of_spatial_partitions[-1].rect.right
        self.height = list_of_spatial_partitions[-1].rect.bottom
        self.normal_partition_width = list_of_spatial_partitions[0].rect.width
        self.normal_partition_height = (list_of_spatial_partitions[0]
                                        .rect.height)
        self.width_in_partitions = self.width // self.normal_partition_width
        self.height_in_partitions = self.height // self.normal_partition_height
        self.area_in_partitions = len(self._partitions)
        self.extra_partition_width = (
            self.width - (
                self.normal_partition_width
                * self.width_in_partitions
            )
        )
        self.extra_partition_height = (
            self.height - (
                self.normal_partition_height
                * self.height_in_partitions
            )
        )

    @classmethod
    def from_dimensions(cls, pixels_wide, pixels_tall,
                        partitions_wide, partitions_tall):

        """Generate a list of SpatialPartition objects.

        Create a 2d space, consisting of non-overlapping "spacial
        "partitions" (SpatialPartition).

        For example, if you `from_dimensions(10, 10, 3, 4)`,
        the SpatialPartitionGrid that will be created will have these
        measurements:

          * partitions wide: 3
          * partitions tall: 4
          * Total partitions: 12
          * partition width (pixels): 10
          * partition height (pixels): 10
          * Grid width: 31px
          * Grid height: 41px

        ... and thus it looks like this:

          +---+---+----+
          | 0 | 1 | 2  |
          +---+---+----+
          | 3 | 4 | 5  |
          +---+---+----+
          | 6 | 7 | 8  |
          +---+---+----+
          | 9 | 10| 11 |
          |___|___|____|

        ... then partition 0's topleft coordinate would be 0,0
        and its dimensions are 10x10 pixels. In fact, all of
        the partitions would be 10x10 pixels, with these exceptions,
        which utilize last_partition_extra_width or
        last_partition_extra_height:

          * Partition 2: top left coord is 20,0. Dimensions are
            11x10 pixels. This is because every last partition
            from each row gets last_partition_extra_width (1px) added
            to its width, to compensate for the total
            SpatialPartitionGrid width (31px) having a remainder when
            divided by the number of partitions per row (3), i.e.,
            `partitions_wide`, that is, to bring the total width of
            the row of partitions to 31px.
          * Partition 5: top left coord is 20,10; dimensions: 11x10px.
          * Partition 8: top left coord is 20,20; dimensions: 11x10px.
          * Partition 9: top left coord is 0,30; dimensions: 10x11px.
          * Partition 10: top left coord is 10,30; dimensions: 10x11px.
          * Partition 11: top left coord is 20,30; dimensions: 11x11px.

        I use this above example extensively in the source code's
        comments for this method.

        Arguments:
            pixels_wide (int):
            pixels_tall (int):
            partitions_wide (int):
            partitions_tall (int):

        Returns:
            SpatialPartitionGrid: created from a list of
                SpatialPartitions.

        Examples:
            To continue the example...

            >>> grid = SpatialPartitionGrid.from_dimensions(
            ...     pixels_wide=31,
            ...     pixels_tall=41,
            ...     partitions_wide=3,
            ...     partitions_tall=4,
            ... )
            >>> len(grid._partitions)
            12
            >>> grid._partitions[0].rect.topleft
            (0, 0)
            >>> grid._partitions[0].rect.size
            (10, 10)
            >>> grid._partitions[11].rect.topleft
            (20, 30)
            >>> grid._partitions[11].rect.size
            (11, 11)
            >>> grid._partitions[5].rect.topleft
            (20, 10)
            >>> grid._partitions[5].rect.size
            (11, 10)
            >>> grid.width
            31
            >>> grid.height
            41
            >>> grid.width_in_partitions
            3
            >>> grid.height_in_partitions
            4
            >>> grid.normal_partition_width
            10
            >>> grid.normal_partition_height
            10
            >>> grid.extra_partition_height
            1
            >>> grid.extra_partition_width
            1

        """

        partition_width = pixels_wide // partitions_wide
        partition_height = pixels_tall // partitions_tall

        # ... We need to add "extra" pixels, in terms of size, to
        # the last partition of every row and to every partition of
        # the last row. This is in case the SpartialPartitionGrid
        # cannot be divided evenly, and we add the remainder pixels
        # to the last partition of every row, and the bottom of every
        # partition of the last row.
        last_partition_extra_width = (pixels_wide - (partitions_wide
                                                     * partition_width))
        last_partition_extra_height = (pixels_tall - (partitions_tall
                                                      * partition_height))

        # We build the partitions, we know how many partitions we need
        # to generate: the grid's area in partitions. So, we iterate
        # through the indexes 0-n for each of those partitions. None
        # of the partitions overlap. Please reference this method's
        # docstring.
        area_in_partitions = partitions_wide * partitions_tall
        list_of_spatial_partitions = []
        for partition_index in six.moves.range(area_in_partitions):
            # if we continue the docstring example, if `partition_index` is
            # 8, its top left coord is 20,20; this calculation will correctly
            # deduce 20 (pixels) for the partition's top left X coordinate.
            #                 2
            # ... as 20 == (8 % 3) * 10
            partition_x = (partition_index % partitions_wide) * partition_width

            # ... again, if `partition_index` is 8 the topleft coord is 20,20,
            # this calculation will correctly deduce 20 (pixels) for this
            # partition's top left Y coordinate.
            #                 2
            # ... as 20 == (8 // 3) * 10
            partition_y = ((partition_index // partitions_wide)
                           * partition_height)

            # The rest of this iteration is devoted to determining the
            # partition's width and height in pixels. By default, the
            # width and height of any partition is 10x10 pixels, but
            # as noted earlier, we need to compensate if there's a
            # remainder when dividing the total grid height/width in
            # pixels by the number of partitions (wide/tall), which the
            # grid consists of.
            #
            # So we start at the standard 10x10 pixel dimensions for the
            # partition, and we later add the compensating pixels if
            # on an appropriate partition to do so.
            this_partitions_width = partition_width
            this_partitions_height = partition_height

            # ... if this is partition index 8: (8 + 1) % 3 == 0
            # tells us that this partition is flush with the right
            # side and thus needs to compensate to stretch to the
            # total SpatialPartitionGrid width in pixels...
            if (partition_index + 1) % partitions_wide == 0:
                # ... if index 8, this will correctly give us
                # the width of 11.
                this_partitions_width += last_partition_extra_width

            # The calculation below tells us if we're on the last
            # row or not, in order to compensate/stretch.
            if partition_index >= area_in_partitions - partitions_wide:
                this_partitions_height += last_partition_extra_height

            # Finally, we've gotten all the info required to accurately
            # create this spacial partition and add it to the list of
            # spatial partitions to return!
            spatial_partition = SpatialPartition(
                x=partition_x,
                y=partition_y,
                width=this_partitions_width,
                height=this_partitions_height,
            )
            list_of_spatial_partitions.append(spatial_partition)

        return SpatialPartitionGrid(
            list_of_spatial_partitions,
        )

    def pixel_coordinates_to_partition(self, x, y):
        """

        Examples:
            To continue the example...

            >>> grid = SpatialPartitionGrid.from_dimensions(
            ...     pixels_wide=31,
            ...     pixels_tall=41,
            ...     partitions_wide=3,
            ...     partitions_tall=4,
            ... )
            >>> lol = grid.pixel_coordinates_to_partition(x=25, y=34)
            >>> lol is grid._partitions[-1]
            True

        """

        new_x = x // self.normal_partition_width
        new_y = y // self.normal_partition_height
        index = (new_x + (new_y * self.width_in_partitions))
        return self._partitions[index]

    # FIXME
    def intersecting_partitions(self, pygame_rect):
        """Return the partitions which a rectangle occupies.

        Warning:
            Since this just checks a rectangles's four
            corners, it will not work properly if the
            rectangle is greater than two partitions in size.

        Arguments:
            pygame_rect (pygame.Rect): ...

        Returns:
            set(SpatialPartition): ...

        Examples:
            >>> grid = SpatialPartitionGrid.from_dimensions(
            ...     pixels_wide=31,
            ...     pixels_tall=41,
            ...     partitions_wide=3,
            ...     partitions_tall=4,
            ... )
            >>> rect = pygame.Rect(15, 25, 10, 10)
            >>> rect.topleft
            (15, 25)
            >>> parts = grid.intersecting_partitions(rect)
            >>> len(parts)
            4

        """

        if ((pygame_rect.width > self.normal_partition_width * 2)
           or (pygame_rect.height > self.normal_partition_height * 2)):
            # update this part to get the partitions in between, in the future
            message = 'Rect must not exceed 2x height nor width. Support soon!'
            raise NotImplementedError(message)
        else:
            return set([
                self.pixel_coordinates_to_partition(*pygame_rect.topleft),
                self.pixel_coordinates_to_partition(*pygame_rect.bottomleft),
                self.pixel_coordinates_to_partition(*pygame_rect.topright),
                self.pixel_coordinates_to_partition(*pygame_rect.bottomright),
            ])

    # FIXME/TODO
    def partitions_for_sprite(self, sprite):

        sprite_position
        # get the index
        asdf
        pass

    # FIXME/TODO
    def move_sprite(self, some_sprite):
        pass

    # FIXME/TODO
    def update_sprite_location(self, some_sprite):
        some_sprite._partitions = asdf

    # FIXME/TODO
    def add_sprites(self, *args):

        for sprite in args:
            sprite._partitions = self.intersecting_partitions(sprite.rect)


# TODO: this is pretty unnecessary now...
def collides_rect(sprite, sprite_group):
    """

    Boilerplate for checking rectangular collision of provided
    sprite against sprites in the provided sprite_group.

    """

    return pygame.sprite.spritecollide(sprite, sprite_group, False)


# TODO: rename; this adds a mask if missing, so
# add_mask_if_missing()
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


if __name__ == '__main__':
    doctest.testmod()
