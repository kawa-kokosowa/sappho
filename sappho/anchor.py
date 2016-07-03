import numpy
import collections


class AnchorPoint(collections.namedtuple('Coordinate', ['x', 'y'])):
    """A coordinate on a surface which is used for pinning to another
    surface Anchor. Used when attempting to afix one surface to
    another, lining up their corresponding anchors.

    Attributes:
        x (int): x-axis coordinate on a surface to place anchor at
        y (int): y-axis coordinate on a surface to place anchor at

    Example:
        >>> anchor = AnchorPoint(5, 3)
        >>> anchor.x
        5
        >>> anchor.y
        3
        >>> coordinate_tuple = (1, 2)
        >>> anchor = AnchorPoint(*coordinate_tuple)
        >>> anchor.x
        1
        >>> anchor.y
        2
        >>> x, y = anchor

    """

    def __repr__(self):
        """Represent the class/anchor with its coordinates.

        Example:
            >>> anchor = AnchorPoint(1, 2)
            >>> print(anchor)
            <AnchorPoint at (1, 2)>

        """

        return "<AnchorPoint at (%d, %d)>" % (self.x, self.y)

    def __add__(self, coordinates):
        """Adds X-Y coordinates to the coordinates of an AnchorPoint.

        Args:
            coordinates (Union[Anchor|Tuple[int, int]]):
                The X-Y coordinates to add to the coordinates
                of the current AnchorPoint. The argument may be
                another AnchorPoint object or tuple of two integers.

        Returns:
            AnchorPoint: A new AnchorPoint with the coordinates of
                the first and second added together.

        Examples:
            >>> coord = AnchorPoint(9, 9)
            >>> other_coord = (5, 5)
            >>> coord + other_coord
            AnchorPoint(14, 14)
            >>> coord = (1, 1)
            >>> other_coord = AnchorPoint(4, 4)
            >>> coord + other_coord
            AnchorPoint(5, 5)

        """

        return AnchorPoint(*numpy.add(coordinates, self))

    def __radd__(self, coordinates):
        """Implements addition when the Anchor is the right-hand operand.
        See Also: `Anchor.__add__()`

        Example:
            >>> coordinates = (1, 2)
            >>> anchor = Anchor(100, 200)
            >>> coordinates + anchor
            <Anchor at (101, 202)>

        """

        return self.__add__(coordinates)

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

        Examples:
            >>> coord = AnchorPoint(9, 9)
            >>> other_coord = (5, 5)
            >>> coord - other_coord
            AnchorPoint(4, 4)
            >>> coord = (1, 1)
            >>> other_coord = AnchorPoint(4, 4)
            >>> coord - other_coord
            AnchorPoint(3, 3)

        """

        return AnchorPoint(*numpy.subtract(coordinates, self))

    def __rsub__(self, coordinates):
        """Implements subtraction when the Anchor is the right-hand operand.

        Example:
            >>> coordinates = (100, 200)
            >>> anchor = Anchor(1, 1)
            >>> coordinates - anchor
            <Anchor at (99, 199)>

        See Also: `Anchor.__sub__()`

        """

        return self.__sub__(coordinates)
