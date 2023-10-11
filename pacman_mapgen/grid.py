# Not using dataclass to keep compatibility with older Python
from __future__ import annotations

from enum import Enum
from types import MappingProxyType
from typing import List, Tuple
from pacman_mapgen.core import CellType, Layout, Position


class Direction(Position, Enum):
    LEFT = Position(x=-1, y=0)
    RIGHT = Position(x=1, y=0)
    UP = Position(x=0, y=-1)
    DOWN = Position(x=0, y=1)

    def reverse(self) -> Direction:
        """Get reverse direction."""
        return _REVERSE_DIRECTIONS[self]


_REVERSE_DIRECTIONS = MappingProxyType(
    {
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
    }
)


class Cell(object):
    """Represents a layout cell."""

    def __init__(self, cell_type: CellType = CellType.EMPTY) -> None:
        self._walls = {direction: True for direction in Direction}
        self.type = cell_type

    def open_wall(self, direction: Direction) -> None:
        self._walls[direction] = False

    def is_open(self, direction: Direction) -> bool:
        return not self._walls[direction]


class CellGrid(object):
    """2D cell grid class.

    Provides a convenient way to interact with cells using Position
    objects rathern than directly accessing the underlaying data
    structure.
    """

    def __init__(
        self, width: int, height: int, init_type: CellType = CellType.EMPTY
    ) -> None:
        self.width = width
        self.height = height
        self._grid = [
            [Cell(cell_type=init_type) for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def __getitem__(self, position: Position) -> Cell:
        """Get cell.

        Args:
            positon: Cell to query.

        Returns:
            Cell at `position`.
        """
        return self._grid[position.y][position.x]

    def get_neighbors(
        self,
        position: Position,
    ) -> List[Tuple[Position, Direction]]:
        """Neighbor positions and direction pairs."""
        all_neighbors = [(position + direction, direction) for direction in Direction]
        return [
            neighbor
            for neighbor in all_neighbors
            if not self.is_out_of_bounds(neighbor[0])
        ]

    def is_out_of_bounds(self, position: Position) -> bool:
        """Tests whether a position is or not out of bounds.

        Args:
            position: Position to evaluate.

        Returns:
            True if it is out of bounds, otherwise False.
        """
        return (
            position.y < 0
            or position.y >= self.height
            or position.x < 0
            or position.x >= self.width
        )

    def open_wall(
        self,
        position: Position,
        direction: Direction,
    ) -> None:
        """Opens the wall that connects `position` with its left.

        Args:
            position: Cell to open.
        """
        neighbor = position + direction
        if self.is_out_of_bounds(position) or self.is_out_of_bounds(neighbor):
            raise IndexError(
                "Cannot open wall as it goes out of bounds",
            )

        self[position].open_wall(direction)
        self[neighbor].open_wall(direction.reverse())

    def to_layout(self) -> Layout:
        layout = Layout(
            width=2 * self.width + 1,
            height=2 * self.height + 1,
            init_type=CellType.WALL,
        )
        for y_pos, row in enumerate(self._grid):
            for x_pos, cell in enumerate(row):
                grid_p = Position(x=x_pos, y=y_pos)
                layout_p = Position(x=2 * x_pos + 1, y=2 * y_pos + 1)

                cell = self[grid_p]
                layout[layout_p] = cell.type

                if cell.is_open(Direction.LEFT):
                    layout[layout_p.left] = CellType.EMPTY
                if cell.is_open(Direction.RIGHT):
                    layout[layout_p.right] = CellType.EMPTY
                if cell.is_open(Direction.UP):
                    layout[layout_p.up] = CellType.EMPTY
                if cell.is_open(Direction.DOWN):
                    layout[layout_p.down] = CellType.EMPTY

        return layout
