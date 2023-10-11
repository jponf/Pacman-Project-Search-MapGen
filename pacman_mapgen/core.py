from __future__ import annotations

import argparse
import sys

from enum import Enum
from random import Random
from types import MappingProxyType
from typing import IO, Iterator, List, Optional, NamedTuple, Tuple


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
    }
)


class Position(NamedTuple):
    """Layout position."""

    x: int
    y: int

    def __add__(self, other: Position) -> Position:
        return Position(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(x=self.x - other.x, y=self.y - other.y)

    @property
    def left(self) -> Position:
        """Position to the left of `self`."""
        return Position(x=self.x - 1, y=self.y)

    @property
    def right(self) -> Position:
        """Position to the right of `self`."""
        return Position(x=self.x + 1, y=self.y)

    @property
    def up(self) -> Position:
        """Position above `self`."""
        return Position(x=self.x, y=self.y - 1)

    @property
    def down(self) -> Position:
        """position below `self`."""
        return Position(x=self.x, y=self.y + 1)


class Layout(object):
    """2D layout class.

    Provides a convenient way to interact with cells using Position
    objects rathern than directly accessing the underlaying data
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
            positon: Cell to query.

        Returns:
            Cell type.
        """
        return self._layout[position.y][position.x]

    def __setitem__(self, position: Position, cell_type: CellType) -> None:
        """Set cell type.

        Args:
            positon: Cell to modify.
            cell_type: New cell type.
        """
        self._layout[position.y][position.x] = cell_type

    def __iter__(self) -> Iterator[Tuple[CellType, ...]]:
        return (tuple(row) for row in self._layout)

    def is_border(self, position: Position) -> bool:
        """Tests if the given position is a border or not.

        Return:
            True if `(x_pos, y_pos)` is a border cell otherwise False.
        """
        return (
            position.x == 0
            or position.x == self.height - 1
            or position.y == 0
            or position.y == self.width - 1
        )

    def is_out_of_bounds(self, position: Position) -> bool:
        return (
            position.y < 0
            or position.y >= self.height
            or position.x < 0
            or position.x >= self.width
        )

    def print(
        self,
        stream: Optional[IO[str]] = None,
    ) -> None:
        """Prints a map layout into the given stream.

        Args:
            layout: The map to print.
            stream: The IO stream where the map will be printed.
                Defaults to sys.stdout.
        """
        stream = stream or sys.stdout

        for row in self:
            for cell_value in row:
                stream.write(CellTypeToAscii.get(cell_value, "u"))

            stream.write("\n")
        stream.flush()


class LayoutGenerator:
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

    def generate_layout(self) -> Layout:
        """Generates a new Map.

        Returns:
            A list of list (num rows x num columns) with the generated map.
        """
        raise NotImplementedError(
            "Layout generator does not implement generate_map",
        )

    def random_position(self, no_border: bool = True) -> Position:
        """Generates a random position.

        The generated positon will never fall in the first nor the last
        row or column, as these are usually reserved for walls.

        Args:
            no_border: Avoid border positions.

        Returns:
            A tuple containing the new position (x_pos, y_pos).
        """
        rand_pos = Position(
            x=self.rand.randint(1, self.height - 2),
            y=self.rand.randint(1, self.width - 2),
        )

        while self.is_border(rand_pos) and no_border:
            rand_pos = Position(
                self.rand.randint(1, self.height - 2),
                self.rand.randint(1, self.width - 2),
            )

        return rand_pos

    def random_positions(self, count: int, no_border: bool = True) -> List[Position]:
        """Generaets `count` distinct random positions.

        Args:
            count: Number of positions to generate.
            no_border: Avoid border positions.

        Returns:
            A list with `count` distinct positions.
        """
        # We should validate count is not too big!
        positions = []
        while len(positions) < count:
            position = self.random_position(no_border=no_border)
            if position not in positions:
                positions.append(position)
        return positions

    def is_border(self, position: Position) -> bool:
        """Tests if the given position is a border or not.

        Return:
            True if `(x_pos, y_pos)` is a border cell otherwise False.
        """
        return (
            position.x == 0
            or position.x == self.height - 1
            or position.y == 0
            or position.y == self.width - 1
        )

    def is_out_of_bounds(self, position: Position) -> bool:
        return (
            position.x < 0
            or position.y >= self.height
            or position.y < 0
            or position.y >= self.width
        )
