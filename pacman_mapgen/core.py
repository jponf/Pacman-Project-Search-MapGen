from __future__ import annotations

import abc
import sys
from enum import Enum
from random import Random
from types import MappingProxyType
from typing import IO, Iterator, List, Tuple


class CellType(Enum):
    """Cell type values."""

    EMPTY = 0
    WALL = 1
    FOOD = 2
    PACMAN = 3


CellTypeToAscii = MappingProxyType(
    {
        CellType.EMPTY: " ",
        CellType.WALL: "%",
        CellType.FOOD: ".",
        CellType.PACMAN: "P",
    },
)


# Not using namedtuple as it causes type conflicts when
# overriding __add__ and __sub__ which are defined in the
# Tuple super-class.
class Position(object):
    """2D position."""

    __slots__ = ("x_coord", "y_coord")

    def __init__(self, x_coord: int, y_coord: int) -> None:
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __eq__(self, other: object) -> bool:
        """Compares two Position objects for equality.

        Args:
            other: Position to compare to `self`.

        Returns:
            True if `self` and `other` have the same coordinates.
        """
        if isinstance(other, Position):
            return self.x_coord == other.x_coord and self.y_coord == other.y_coord

        return False

    def __hash__(self) -> int:
        """Computes a hash value representing this position.

        Returns:
            A hash value computed from `self`'s information.
        """
        return hash(
            (
                self.x_coord,
                self.y_coord,
            ),
        )  # Lazy :)

    def __add__(self, other: Position) -> Position:
        """Adds the coordinates of two positions.

        Args:
            other: Position coordinates to add to `self`.

        Returns:
            A new position resulting of adding the coordinate components.
        """
        return Position(
            x_coord=self.x_coord + other.x_coord,
            y_coord=self.y_coord + other.y_coord,
        )

    def __sub__(self, other: Position) -> Position:
        """Subtracts the coordinates of two positions.

        Args:
            other: Position coordinates to subtract to `self`.

        Returns:
            A new position resulting of subtracting the coordinate components.
        """
        return Position(
            x_coord=self.x_coord + other.x_coord,
            y_coord=self.y_coord + other.y_coord,
        )

    def __repr__(self) -> str:
        """String representation of an instance of Position.

        Returns:
            A string representing `self`.
        """
        return "{0}(x_coord={1}, y_coord={2})".format(
            self.__class__.__name__,
            self.x_coord,
            self.y_coord,
        )

    @property
    def left(self) -> Position:
        """Position to the left.

        Returns:
            Position to the left of `self`.
        """
        return Position(x_coord=self.x_coord - 1, y_coord=self.y_coord)

    @property
    def right(self) -> Position:
        """Position to the right.

        Returns:
            Position to the right of `self`.
        """
        return Position(x_coord=self.x_coord + 1, y_coord=self.y_coord)

    @property
    def up(self) -> Position:
        """Position above.

        Returns:
            Position above `self`.
        """
        return Position(x_coord=self.x_coord, y_coord=self.y_coord - 1)

    @property
    def down(self) -> Position:
        """Position below.

        Returns:
            Position below `self`.
        """
        return Position(x_coord=self.x_coord, y_coord=self.y_coord + 1)


class Layout(object):
    """Represents a 2D Pac-Man project layout.

    Provides a convenient way to interact with cells using Position
    objects rather than directly accessing the underlying data
    structure.
    """

    def __init__(
        self,
        width: int,
        height: int,
        init_type: CellType,
    ) -> None:
        self.width = width
        self.height = height
        self._layout = [
            [init_type for _ in range(self.width)] for _ in range(self.height)
        ]

    def __getitem__(self, position: Position) -> CellType:
        """Get cell type.

        Args:
            position: Cell to query.

        Returns:
            Cell type.
        """
        return self._layout[position.y_coord][position.x_coord]

    def __setitem__(self, position: Position, cell_type: CellType) -> None:
        """Set cell type.

        Args:
            position: Cell to modify.
            cell_type: New cell type.
        """
        self._layout[position.y_coord][position.x_coord] = cell_type

    def __iter__(self) -> Iterator[Tuple[CellType, ...]]:
        """Iterator over the rows of the layout.

        Returns:
            An iterator that returns the rows of the layout
            as tuples of cells.
        """
        return (tuple(row) for row in self._layout)

    def is_border(self, position: Position) -> bool:
        """Tests if the given position is a border or not.

        Args:
            position: Position to evaluate.

        Returns:
            True if `position` is a border cell otherwise False.
        """
        return (
            position.x_coord == 0
            or position.x_coord == self.height - 1
            or position.y_coord == 0
            or position.y_coord == self.width - 1
        )

    def print(
        self,
        stream: IO[str] = sys.stdout,
    ) -> None:
        """Prints a map layout into the given stream.

        Args:
            stream: The IO stream where the map will be printed.
        """
        for row in self:
            for cell_value in row:
                stream.write(CellTypeToAscii.get(cell_value, "u"))

            stream.write("\n")
        stream.flush()


class LayoutGenerator(abc.ABC):
    """Layout generator.

    Args:
        num_rows: Number of rows.
        num_cols: Number of columns.
        seed: To initialize the random number generator.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: int,
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.rand = Random(self.seed)

        if self.width <= 2:
            raise ValueError("Number of rows must be greater than 2")
        if self.height <= 2:
            raise ValueError("Number of columns must be greater than 2")

    @abc.abstractmethod
    def generate_layout(self) -> Layout:
        """Generates a new Map.

        Returns:
            A list of list (num rows x num columns) with the generated map.
        """  # noqa: DAR202

    def random_position(self, no_border: bool = True) -> Position:
        """Generates a random position.

        The generated position will never fall in the first nor the last
        row or column, as these are usually reserved for walls.

        Args:
            no_border: Avoid border positions.

        Returns:
            A tuple containing the new position (x_pos, y_pos).
        """
        rand_pos = Position(
            x_coord=self.rand.randint(1, self.height - 2),
            y_coord=self.rand.randint(1, self.width - 2),
        )

        while self.is_border(rand_pos) and no_border:
            rand_pos = Position(
                self.rand.randint(1, self.height - 2),
                self.rand.randint(1, self.width - 2),
            )

        return rand_pos

    def random_positions(self, count: int, no_border: bool = True) -> List[Position]:
        """Generates `count` distinct random positions.

        Args:
            count: Number of positions to generate.
            no_border: Avoid border positions.

        Returns:
            A list with `count` distinct positions.
        """
        # We should validate count is not too big!
        positions: List[Position] = []
        while len(positions) < count:
            position = self.random_position(no_border=no_border)
            if position not in positions:
                positions.append(position)
        return positions

    def is_border(self, position: Position) -> bool:
        """Tests if the given position is a border or not.

        Args:
            position: Position to evaluate.

        Returns:
            True if `position` is located at the border, otherwise False.
        """
        return (
            position.x_coord == 0
            or position.x_coord == self.height - 1
            or position.y_coord == 0
            or position.y_coord == self.width - 1
        )

    def is_out_of_bounds(self, position: Position) -> bool:
        """Tests whether a position is out of bounds.

        Args:
            position: Position to evaluate.

        Returns:
            True if it is out of bounds, otherwise False.
        """
        return (
            position.x_coord < 0
            or position.y_coord >= self.height
            or position.y_coord < 0
            or position.y_coord >= self.width
        )
