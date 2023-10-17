from pacman_mapgen.core import CellType, Layout, LayoutGenerator
from pacman_mapgen.grid import CellGrid


class RandomizedDfsLayoutGenerator(LayoutGenerator):
    """Layout generator based on randomized DFS search.

    Due to the layout construction procedure the final result
    will have `2 * width + 1` columns and `2 * height + 1` rows.
    """

    def generate_layout(self) -> Layout:
        """Generate a layout traversing the map using a randomized DFS.

        At every step we expand the last node in the fringe, adding the
        neighbors in random order every time.

        Returns:
            A layout with the corridors generated using a randomized
            DFS exploration strategy.
        """
        grid = CellGrid(width=self.width, height=self.height)
        position = self.random_position()
        neighbors = grid.get_neighbors(position)

        if not neighbors:  # Nothing to explore
            return grid.to_layout()

        fringe = [(position, neighbors)]
        visited = {position}

        while fringe:
            position, neighbors = fringe[-1]
            neighbor, direction = neighbors.pop()

            # Last neighbor removed, no need to re-explore
            if not neighbors:
                fringe.pop()

            if neighbor not in visited:
                grid.open_wall(position, direction)
                visited.add(neighbor)
                next_neighbors = grid.get_neighbors(neighbor)

                if next_neighbors:
                    self.rand.shuffle(next_neighbors)
                    fringe.append((neighbor, next_neighbors))

        # Place pacman and food
        pacman_pos, food_pos = self.random_positions(count=2, no_border=False)
        grid[pacman_pos].type = CellType.PACMAN
        grid[food_pos].type = CellType.FOOD

        return grid.to_layout()
