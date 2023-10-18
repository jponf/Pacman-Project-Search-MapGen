import itertools

from pacman_mapgen.core import (CellGrid, CellType, Layout, LayoutGenerator,
                                Position)


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
        if self.wall_probability <= 0 or self.wall_probability > 1.0:  # noqa: WPS459
            raise ValueError("Wall probability must be between 0 and 1")

    def _generate_plain_layout(self, grid: CellGrid) -> Layout:
        """Generate a layout assigning walls with random probability.

        The generated map is not guaranteed to have a solution.

        Returns:
            A layout generated by randomly setting walls.
        """
        # pacman_pos, food_pos = self.random_positions(count=2)

        # grid = CellGrid(
        #     width=self.width,
        #     height=self.height,
        #     init_type=CellType.EMPTY,
        # )
        # grid[pacman_pos].type = CellType.PACMAN
        # grid[food_pos].type = CellType.FOOD

        for x_pos, y_pos in itertools.product(  # noqa: WPS352
            range(self.width),
            range(self.height),
        ):
            position = Position(x_coord=x_pos, y_coord=y_pos)
            for _, direction in grid.get_neighbors(position):
                if self.rand.random() < self.wall_probability:
                    grid.open_wall(position, direction)

        return grid.to_layout()
