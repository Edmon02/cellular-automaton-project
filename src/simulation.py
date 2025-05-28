# src/simulation.py
from grid import Grid
from entities import Entity
from rules import Rules


class Simulation:
    def __init__(self, width: int, height: int):
        self.grid = Grid(width, height)
        self.entities = [
            Entity(2 * width // 4, height // 4, (17, 74, 88), typeE=1),  # Black dot
            Entity(3 * width // 4, 3 * height // 4, (216, 231, 226), typeE=0),  # White dot
        ]
        self.rules = Rules()
        self.day_count = 0
        self.night_count = 0

    def step(self):
        """Run one iteration of the simulation."""
        for entity in self.entities:
            self.rules.move_entity(entity, self.grid)
        self.day_count, self.night_count = self.rules.update_counts(
            self.grid, self.day_count, self.night_count
        )
