# Not using dataclass to keep compatibility with older Python
from __future__ import annotations

from enum import Enum
from types import MappingProxyType
from typing import List, Tuple

from pacman_mapgen.core import CellType, Layout, Position


class Direction(Position, Enum):
    """Direction from a position.

    These constants can be added to a Position to obtain
    the position resulting from taking that action from
    that position.
    """

    # Implicit call to __init__(x_coord, y_coord)
    LEFT = -1, 0
    RIGHT = 1, 0
    UP = 0, -1
    DOWN = 0, 1

    def reverse(self) -> Direction:
        """Get reverse direction.

        Returns:
            Direction that reverses `self`.
        """
        return _REVERSE_DIRECTIONS[self]


_REVERSE_DIRECTIONS = MappingProxyType(
    {
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
    },
)


class Cell(object):
    """Represents a layout cell."""

    def __init__(self, cell_type: CellType = CellType.EMPTY) -> None:
        self._walls = {direction: True for direction in Direction}
        self.type = cell_type

    def open_wall(self, direction: Direction) -> None:
        """Marks the wall open.

        Args:
            direction: Direction of the wall that must be marked as open.
        """
        self._walls[direction] = False

    def is_open(self, direction: Direction) -> bool:
        """Tests whether the wall is open or not.

        Args:
            direction: Direction of the wall that is being tested.

        Returns:
            True if the wall going `direction` is open, otherwise False.
        """
        return not self._walls[direction]


class CellGrid(object):
    """2D cell grid class.

    Provides a convenient way to interact with cells using Position
    objects rather than directly accessing the underlying data
    structure. Moreover, it has a convenient method to create a layout
    that "looks" nice, from the grid cells values and walls.
    """

    def __init__(
        self,
        width: int,
        height: int,
        init_type: CellType = CellType.EMPTY,
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
            position: Cell to query.

        Returns:
            Cell at `position`.
        """
        return self._grid[position.y_coord][position.x_coord]

    def get_neighbors(
        self,
        position: Position,
    ) -> List[Tuple[Position, Direction]]:
        """Neighbor positions and direction pairs.

        Args:
            position: Position of the cell from which the neighbors
                are going to be computed.

        Returns:
            Neighbors as a list of pairs (position, direction).
        """
        all_neighbors = [(position + direction, direction) for direction in Direction]
        return [
            neighbor
            for neighbor in all_neighbors
            if not self.is_out_of_bounds(neighbor[0])
        ]

    def is_out_of_bounds(self, position: Position) -> bool:
        """Tests whether a position is out of bounds.

        Args:
            position: Position to evaluate.

        Returns:
            True if it is out of bounds, otherwise False.
        """
        return (
            position.y_coord < 0
            or position.y_coord >= self.height
            or position.x_coord < 0
            or position.x_coord >= self.width
        )

    def open_wall(
        self,
        position: Position,
        direction: Direction,
    ) -> None:
        """Opens the wall that connects position with its neighbor.

        Args:
            position: Cell to open.
            direction: Direction of the wall from `position` to open.

        Raises:
            IndexError: If `direction` from `position` goes out of bounds.
        """
        neighbor = position + direction
        if self.is_out_of_bounds(position) or self.is_out_of_bounds(neighbor):
            raise IndexError(
                "Cannot open wall as it goes out of bounds",
            )

        self[position].open_wall(direction)
        self[neighbor].open_wall(direction.reverse())

    def to_layout(self) -> Layout:
        """Creates a layout from the grid.

        Returns:
            A layout object constructed using information from
            the grid cells.
        """
        layout = Layout(
            width=2 * self.width + 1,
            height=2 * self.height + 1,
            init_type=CellType.WALL,
        )
        for y_pos, row in enumerate(self._grid):
            for x_pos, cell in enumerate(row):
                layout_p = Position(x_coord=2 * x_pos + 1, y_coord=2 * y_pos + 1)

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
