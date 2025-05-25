# src/grid.py
import numpy as np


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # 0 = day (light), 1 = night (dark)
        self.cells = np.zeros((height, width), dtype=int)
        self.initialize_split_grid()

    def initialize_split_grid(self):
        """Initialize the grid with 0s on the left half and 1s on the right half."""
        mid_point = self.width // 2
        self.cells[:, mid_point:] = 1  # Fill right side with 1s

    def toggle_cell(self, x, y):
        """Toggle the state of a cell."""
        self.cells[y, x] = 1 - self.cells[y, x]

    def get_state(self, x, y):
        """Get the state of a cell."""
        return self.cells[y, x]

    def reset(self):
        """Reset the grid to all day (light)."""
        self.cells.fill(0)
