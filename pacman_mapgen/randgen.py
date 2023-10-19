import itertools

from pacman_mapgen.core import CellGrid, LayoutGenerator, Position


class RandomLayoutGenerator(LayoutGenerator):
    """Simple random layout generator."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int,
        cycle_probability: float,
        wall_probability: float,
    ) -> None:
        super().__init__(
            width=width,
            height=height,
            seed=seed,
            cycle_probability=cycle_probability,
        )
        self.wall_probability = wall_probability
        if self.wall_probability <= 0 or self.wall_probability > 1.0:  # noqa: WPS459
            raise ValueError("Wall probability must be between 0 and 1")

    def _create_paths(self, grid: CellGrid) -> None:
        """Opens paths with random probability.

        The generated map is not guaranteed to have a solution.

        Args:
            grid: Grid to generate the layout with
        """
        for x_pos, y_pos in itertools.product(  # noqa: WPS352
            range(self.width),
            range(self.height),
        ):
            position = Position(x_coord=x_pos, y_coord=y_pos)
            for _, direction in grid.get_neighbors(position):
                if self.rand.random() < self.wall_probability:
                    grid.open_wall(position, direction)
