from pacman_mapgen.core import CellType, Layout, LayoutGenerator, Position
from pacman_mapgen.grid import CellGrid


class RandomLayoutGenerator(LayoutGenerator):
    """Simple random layout generator."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int,
        wall_probability: float,
    ) -> None:
        super().__init__(
            width=width,
            height=height,
            seed=seed,
        )
        self.wall_probability = wall_probability
        if not 0 <= self.wall_probability <= 1.0:
            raise ValueError("Wall probability must be between 0 and 1")

    def generate_layout(self) -> Layout:
        """Generate a layout assigning walls with random probability.

        The generated map is not guaranteed to have a solution.
        """
        pacman_pos, food_pos = self.random_positions(count=2)

        grid = CellGrid(
            width=self.width,
            height=self.height,
            init_type=CellType.EMPTY,
        )
        grid[pacman_pos].type = CellType.PACMAN
        grid[food_pos].type = CellType.FOOD

        for y_pos in range(self.width):
            for x_pos in range(self.height):
                position = Position(x=x_pos, y=y_pos)
                for _, direction in grid.get_neighbors(position):
                    if self.rand.random() < self.wall_probability:
                        grid.open_wall(position, direction)

        return grid.to_layout()
