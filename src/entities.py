# src/entities.py
class Entity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color  # e.g., (0, 0, 0) for black, (255, 255, 255) for white

    def move(self, dx, dy, grid):
        """Move the entity with boundary checking."""
        new_x = (self.x + dx) % grid.width
        new_y = (self.y + dy) % grid.height
        self.x, self.y = new_x, new_y
