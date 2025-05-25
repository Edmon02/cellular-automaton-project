# tests/test_grid.py
import unittest
from src.grid import Grid


class TestGrid(unittest.TestCase):
    def test_toggle_cell(self):
        grid = Grid(5, 5)
        grid.toggle_cell(2, 2)
        self.assertEqual(grid.get_state(2, 2), 1)
        grid.toggle_cell(2, 2)
        self.assertEqual(grid.get_state(2, 2), 0)


if __name__ == "__main__":
    unittest.main()
