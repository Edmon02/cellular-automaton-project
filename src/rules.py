# src/rules.py
import random
import numpy as np


class Rules:
    def __init__(self):
        self.directions = [
            (-1, -1),
            (1, -1),
            (-1, 1),
            (1, 1),
        ]  # left-up, right-up, left-down, right-down

    def move_entity(self, entity, grid):
        """Move an entity randomly."""
        dx, dy = random.choice(self.directions)
        entity.move(dx, dy, grid)
        # Toggle the cell the entity lands on
        grid.toggle_cell(entity.x, entity.y)
        print(entity.x, entity.y)

    def update_counts(self, grid, day_count, night_count):
        """Update day and night counts based on cell states."""
        night_cells = np.sum(grid.cells)
        day_cells = (grid.width * grid.height) - night_cells
        return day_count + day_cells, night_count + night_cells
