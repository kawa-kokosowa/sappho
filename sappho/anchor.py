class Anchor(object):
    """A coordinate on a surface which is used for pinning to another
    surface Anchor. Used when attempting to afix one surface to
    another, lining up their corresponding anchors.

    Attributes:
        x (int): x-axis coordinate on a surface to place anchor at
        y (int): y-axis coordinate on a surface to place anchor at

    Example:
        >>> anchor = Anchor(5, 3)
        >>> anchor.x
        5
        >>> anchor.y
        3
        >>> coordinate_tuple = (1, 2)
        >>> anchor = Anchor(*coordinate_tuple)
        >>> anchor.x
        1
        >>> anchor.y
        2

    """

    def __init__(self, x, y):
        """Create an Anchor using two integers to
        represent this Anchor's coordinate.

        Args:
            x (int): X-axis position of the supplied
                coordinate in pixels.
            y (int): Y-axis position of the supplied
                coordinate in pixels.

        """

        self.x = x
        self.y = y

    @staticmethod
    def _coords_are_ints(coordinates):
        """Check if a two-element tuple representing 2D
        coordinates consists of two integers.

        This presumes that coordinates is indeed a
        two-element tuple.

        Arguments:
            coordinates (tuple):

        Returns:
            bool: True if the coordinates are integers, False
                otherwise.

        """

        return type(coordinates[0]) == int and type(coordinates[1]) == int

    def __repr__(self):
        """Represent the class/anchor with its coordinates.

        Example:
            >>> anchor = Anchor(1, 2)
            >>> print(anchor)
            <Anchor at (1, 2)>

        """

        return "<Anchor at (%d, %d)>" % (self.x, self.y)

    def __add__(self, coordinates):
        """Adds X-Y coordinates to the coordinates of an Anchor.

        Args:
            coordinates (Union[Anchor|Tuple[int, int]]):
                The X-Y coordinates to add to the coordinates
                of the current Anchor.  The argument may be
                another Anchor object or tuple of two integers.

        Returns:
            Anchor: A new Anchor with the coordinates of
                the first and second added together.

        Raises:
            NotImplemented: If `coordinates` is not an `Anchor`
                or a 2-tuple of integers.

        Example:
            >>> anchor_a = Anchor(4, 1)
            >>> anchor_b = Anchor(2, 0)
            >>> anchor_a + anchor_b
            <Anchor at (6, 1)>
            >>> coordinate_tuple = (10, 20)
            >>> anchor_a + coordinate_tuple
            <Anchor at (14, 21)>
            >>> coordinate_tuple + anchor_a
            <Anchor at (14, 21)>
            >>> anchor_a + 1.5 # doctest: +SKIP
            Traceback (most recent call last):
            TypeError: 'float' object is not subscriptable

        """

        if isinstance(coordinates, Anchor):

            return Anchor(self.x + coordinates.x,
                          self.y + coordinates.y)

        elif self._coords_are_ints(coordinates):

            return Anchor(self.x + coordinates[0],
                          self.y + coordinates[1])

        else:

            raise NotImplementedError(coordinates)

    def __radd__(self, coordinates):
        """Implements addition when the Anchor is the right-hand operand.

        See Also: `Anchor.__add__()`

        Example:
            >>> coordinates = (1, 2)
            >>> anchor = Anchor(100, 200)
            >>> coordinates + anchor
            <Anchor at (101, 202)>

        """

        return self + coordinates

    def __sub__(self, coordinates):
        """Subtracts the given X-Y coordinates from the Anchor.

        Args:
            coordinates (Union[Anchor|Tuple[int, int]]):
                The X-Y coordinates to subtract from the coordinates
                of the current Anchor.  The argument may be another
                Anchor object or tuple of two integers.

        Returns:
            Anchor: A new Anchor with the coordinates of
                the second subtracted from the first.

        Raises:
            NotImplemented: If `coordinates` is not an `Anchor`
                or a 2-tuple of integers.

        Example:
            >>> anchor_a = Anchor(4, 1)
            >>> anchor_b = Anchor(2, 0)
            >>> anchor_a - anchor_b
            <Anchor at (2, 1)>
            >>> coordinate_tuple = (3, 0)
            >>> anchor_a - coordinate_tuple
            <Anchor at (1, 1)>
            >>> coordinate_tuple - anchor_b
            <Anchor at (1, 0)>
            >>> anchor_a - 3.2 # doctest: +SKIP
            Traceback (most recent call last):
            TypeError: 'float' object is not subscriptable

        """

        if isinstance(coordinates, Anchor):

            return Anchor(self.x - coordinates.x,
                          self.y - coordinates.y)

        elif self._coords_are_ints(coordinates):

            return Anchor(self.x - coordinates[0],
                          self.y - coordinates[1])

        else:

            raise NotImplemented

    def __rsub__(self, coordinates):
        """Implements subtraction when the Anchor is the right-hand operand.

        Example:
            >>> coordinates = (100, 200)
            >>> anchor = Anchor(1, 1)
            >>> coordinates - anchor
            <Anchor at (99, 199)>

        See Also: `Anchor.__sub__()`

        """
        # The naive implementation would be...
        #
        #     return self - coordinates
        #
        # ...but that produces the wrong result because subtraction is
        # not commutative.  We also cannot write...
        #
        #     return coordinates - self
        #
        # ...because then we're invoking this method again, i.e. we
        # create a never-ending loop.
        #
        # To deal with this problem we take advantage of the fact that
        # the following mathematical expressions are equivalent for
        # natural numbers:
        #
        #     x - y
        #     (-x) + y
        #
        # Therefore we create a new `Anchor` which is the inverse of
        # the `self`, i.e. the `x` in the example above, and then we
        # *add* the coordinates (`y`) to that, which gives us the
        # correct result.

        return (self * -1) + coordinates

    def __mul__(self, multiplier):
        """Multiplies the X-Y coordinates of an Anchor by an integer.

        Args:
            multiplier (int): The number to multiply to each coordinate.

        Returns:
            Anchor: A new Anchor object with X-Y coordinates multiplied
                by the `multiplier` argument.

        Raises:
            NotImplemented: If `multiplier` is not an integer.

        Example:
            >>> anchor = Anchor(3, 5)
            >>> anchor * -1
            <Anchor at (-3, -5)>
            >>> anchor * 0
            <Anchor at (0, 0)>
            >>> 2 * anchor
            <Anchor at (6, 10)>
            >>> anchor * 1.5 # doctest: +SKIP
            Traceback (most recent call last):
            TypeError: exceptions must derive from BaseException

        """

        if type(multiplier) == int:

            return Anchor(self.x * multiplier, self.y * multiplier)

        else:

            raise NotImplemented

    def __rmul__(self, multiplier):
        """Allows the Anchor to be on the right-hand of multiplication.

        See Also: `Anchor.__mul__()`

        Example:
            >>> 10 * Anchor(1, 2)
            <Anchor at (10, 20)>
            >>> 2.5 * Anchor(0, 0) # doctest: +SKIP
            Traceback (most recent call last):
            TypeError: exceptions must derive from BaseException

        """

        return self * multiplier

    def as_tuple(self):
        """Represent this anchors's (x, y)
        coordinates as a Python tuple.

        Returns:
            tuple(int, int): (x, y) coordinate tuple
                of this Anchor.

        """

        return (self.x, self.y)

