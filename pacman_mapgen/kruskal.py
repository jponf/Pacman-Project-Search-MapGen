from pacman_mapgen.core import CellGrid, LayoutGenerator, Position


class KruskalLayoutGenerator(LayoutGenerator):
    """Layout generator using Kruskal's method.

    Due to the layout construction procedure the final result
    will have `2 * width + 1` columns and `2 * height + 1` rows.
    """

    def _create_paths(self, grid: CellGrid) -> None:  # noqa: WPS210
        """Opens paths using Kruskal's algorithm.

        Args:
            grid: Grid to generate the layout with
        """
        positions = [
            Position(x_coord=x_pos, y_coord=y_pos)
            for x_pos in range(self.width)
            for y_pos in range(self.height)
        ]
        walls = [
            (position, direction)
            for position in positions
            for _, direction in grid.get_neighbors(position)
        ]
        self.rand.shuffle(walls)

        # Keep track of which set the cells belong to
        cell_set = {position: idx for idx, position in enumerate(positions)}
        set_cells = [{position} for position in positions]

        while walls:
            position, direction = walls.pop()
            neighbor = position + direction

            p_set_idx = cell_set[position]
            n_set_idx = cell_set[neighbor]

            if p_set_idx != n_set_idx:
                grid.open_wall(position, direction)
                new_set_idx = min(p_set_idx, n_set_idx)
                new_set = set_cells[p_set_idx].union(set_cells[n_set_idx])
                is_p_set = p_set_idx == new_set_idx

                # All cells from both sets now belong to new_set
                set_cells[p_set_idx] = new_set if is_p_set else set()
                set_cells[n_set_idx] = set() if is_p_set else new_set
                for pos in new_set:
                    cell_set[pos] = new_set_idx

        assert not set_cells[1], "All cells must belong to set 0"  # noqa: S101
