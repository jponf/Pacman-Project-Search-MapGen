from __future__ import annotations

import abc
import sys
from enum import Enum
from random import Random
from types import MappingProxyType
from typing import IO, Iterator, List, Optional, Sequence, Tuple

from pacman_mapgen.utils.type_utils import StrEnum


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

    def fill_with_food(self, max_food: int, rand: Random) -> None:
        """Fills empty layout cells with food.

        Args:
            max_food: Maximum number of food cells to generate.
            rand: Random engine to randomly select empty cells.
        """
        empty_cells = [
            Position(x_coord=x_coord, y_coord=y_coord)
            for y_coord, row in enumerate(self._layout)
            for x_coord, cell in enumerate(row)
            if cell is CellType.EMPTY
        ]
        rand.shuffle(empty_cells)

        max_food = max_food if max_food > 0 else len(empty_cells)
        while max_food > 0 and empty_cells:
            self[empty_cells.pop()] = CellType.FOOD
            max_food -= 1

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


class ProblemType(StrEnum):
    """Pac-Man project problem types."""

    FOOD = "food"
    SEARCH = "search"
    CORNERS = "corners"


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

    def generate_layout(
        self,
        problem_type: ProblemType,
        max_food: int,
    ) -> Layout:
        """Generates a new layout and sets pacman and food.

        Args:
            problem_type: Pac-Man project problem type. Pac-Man and
                foods' location will be set acording to the type.
            max_food: Maximum number of food cells when problem type
                is `ProblemType.Food`.

        Returns:
            A layout object with Pac-Man set accordingly.
        """
        grid = CellGrid(width=self.width, height=self.height)

        if problem_type is ProblemType.SEARCH:
            pacman_pos = self.random_position()
            food_pos = [self.random_position(forbidden=[pacman_pos])]
        elif problem_type is ProblemType.CORNERS:
            food_pos = self.get_corners()
            pacman_pos = self.random_position(forbidden=food_pos)
        elif problem_type is ProblemType.FOOD:
            pacman_pos = self.random_position()
            food_pos = []

        grid[pacman_pos].type = CellType.PACMAN
        for pos in food_pos:
            grid[pos].type = CellType.FOOD

        layout = self._generate_plain_layout(grid)

        # Fill if type is food
        if problem_type is ProblemType.FOOD:
            layout.fill_with_food(max_food=max_food, rand=self.rand)

        return layout  # noqa: WPS331

    def get_corners(self) -> List[Position]:
        """Get grid corner positions.

        Returns:
            List of corner positions
        """
        return [
            Position(x_coord=0, y_coord=0),
            Position(x_coord=0, y_coord=self.height - 1),
            Position(x_coord=self.width - 1, y_coord=0),
            Position(x_coord=self.width - 1, y_coord=self.height - 1),
        ]

    def random_position(
        self,
        no_border: bool = False,
        forbidden: Optional[Sequence[Position]] = None,
    ) -> Position:
        """Generates a random position.

        The generated position will never fall in the first nor the last
        row or column, as these are usually reserved for walls.

        Args:
            no_border: Avoid border positions.
            forbidden: Forbidden positions.

        Returns:
            A tuple containing the new position (x_pos, y_pos).
        """
        forbidden = forbidden or []
        rand_pos = Position(
            x_coord=self.rand.randint(0, self.width - 1),
            y_coord=self.rand.randint(0, self.height - 1),
        )
        not_ok = self.is_border(rand_pos) and no_border
        not_ok = not_ok or rand_pos in forbidden

        while not_ok:
            rand_pos = Position(
                self.rand.randint(1, self.height - 2),
                self.rand.randint(1, self.width - 2),
            )
            not_ok = self.is_border(rand_pos) and no_border
            not_ok = not_ok or rand_pos in forbidden

        return rand_pos

    def random_positions(self, count: int, no_border: bool = False) -> List[Position]:
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

    @abc.abstractmethod
    def _generate_plain_layout(self, grid: CellGrid) -> Layout:
        """Generates a new layout without setting the cell values.

        Args:
            grid: A previously initialized grid.

        Returns:
            A list of list (num rows x num columns) with the generated map.
        """  # noqa: DAR202
