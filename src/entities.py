# src/entities.py
class Entity:
    def __init__(
        self, x: int, y: int, color: tuple, px: int = 0, py: int = 0, typeE: int = -1
    ):
        self.px = px
        self.py = py
        self.x = x
        self.y = y
        self.color = color  # e.g., (0, 0, 0) for black, (255, 255, 255) for white
        self.type = typeE  # Type of the entity for identification

    def move(self, dx: int, dy: int, grid) -> None:
        """Move the entity with boundary checking."""
        new_x: int = (self.x + dx) % grid.width
        new_y: int = (self.y + dy) % grid.height
        self.x, self.y = new_x, new_y
