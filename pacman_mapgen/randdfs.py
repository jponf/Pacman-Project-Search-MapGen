from pacman_mapgen.core import CellGrid, LayoutGenerator


class RandomizedDfsLayoutGenerator(LayoutGenerator):
    """Layout generator based on randomized DFS search.

    Due to the layout construction procedure the final result
    will have `2 * width + 1` columns and `2 * height + 1` rows.
    """

    def _create_paths(self, grid: CellGrid) -> None:
        """Opens path traversing the grid using a randomized DFS.

        At every step we expand the last node in the fringe, adding the
        neighbors in random order every time.

        Args:
            grid: Grid to generate the layout with.
        """
        position = self.random_position()
        neighbors = grid.get_neighbors(position)

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
