from pacman_mapgen.core import CellGrid, CellType, Layout, LayoutGenerator


class PrimLayoutGenerator(LayoutGenerator):
    """Layout generator using Kruskal's method.

    Due to the layout construction procedure the final result
    will have `2 * width + 1` columns and `2 * height + 1` rows.
    """

    def _generate_plain_layout(self) -> Layout:  # noqa: WPS210
        """Generate a layout using Kruskal's algorithm.

        Returns:
            A layout created using Kruskal's algorithm.
        """
        grid = CellGrid(width=self.width, height=self.height)
        cur_pos = self.random_position(no_border=False)
        pending = grid.get_neighbors(cur_pos)
        visited = {cur_pos}

        while pending:
            cur_pos, direction = pending.pop()

            if cur_pos not in visited:
                grid.open_wall(cur_pos, direction.reverse())
                pending.extend(
                    (neighbor, direction)
                    for neighbor, direction in grid.get_neighbors(cur_pos)
                    if neighbor not in visited
                )
                self.rand.shuffle(pending)
                visited.add(cur_pos)

        # Place Pac-Man and food
        pacman_pos, food_pos = self.random_positions(count=2, no_border=False)
        grid[pacman_pos].type = CellType.PACMAN
        grid[food_pos].type = CellType.FOOD

        return grid.to_layout()
