# src/visualization.py
import pygame


class Visualizer:
    def __init__(self, simulation, cell_size=20, show_grid=False, show_coordinates=False):
        self.simulation = simulation
        self.cell_size = cell_size
        self.show_grid = show_grid
        self.show_coordinates = show_coordinates
        self.width = simulation.grid.width * cell_size
        self.height = simulation.grid.height * cell_size
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height + 30)
        )  # Extra space for text
        pygame.display.set_caption("Cellular Automaton Simulation")
        self.font = pygame.font.SysFont(None, 24)

    def draw(self):
        self.screen.fill((200, 200, 200))  # Background)

        # Draw split-screen background
        for y in range(self.simulation.grid.height):
            for x in range(self.simulation.grid.width):
                color = (
                    (216, 231, 226)
                    if self.simulation.grid.get_state(x, y) == 0
                    else (17, 74, 88)
                )
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

        # Draw entities
        for entity in self.simulation.entities:
            pygame.draw.circle(
                self.screen,
                entity.color,
                (
                    entity.x * self.cell_size + self.cell_size // 2,
                    entity.y * self.cell_size + self.cell_size // 2,
                ),
                self.cell_size // 2,
            )

        # Draw grid lines for better coordinate visualization
        if self.show_grid:
            for x in range(self.simulation.grid.width + 1):
                pygame.draw.line(
                    self.screen,
                    (128, 128, 128),
                    (x * self.cell_size, 0),
                    (x * self.cell_size, self.simulation.grid.height * self.cell_size),
                    1,
                )
            for y in range(self.simulation.grid.height + 1):
                pygame.draw.line(
                    self.screen,
                    (128, 128, 128),
                    (0, y * self.cell_size),
                    (self.simulation.grid.width * self.cell_size, y * self.cell_size),
                    1,
                )

        # Draw coordinate labels for debugging
        if self.show_coordinates:
            small_font = pygame.font.SysFont(None, 12)
            for y in range(min(10, self.simulation.grid.height)):  # Only show first 10 for clarity
                for x in range(min(10, self.simulation.grid.width)):
                    coord_text = small_font.render(
                        f"{x},{y}", True, (64, 64, 64)
                    )
                    self.screen.blit(
                        coord_text,
                        (x * self.cell_size + 2, y * self.cell_size + 2),
                    )

        # Draw counters
        text = self.font.render(
            f"day {self.simulation.day_count} | night {self.simulation.night_count}",
            True,
            (0, 0, 0),
        )
        self.screen.blit(text, (10, self.height + 5))
        pygame.display.flip()

    def close(self):
        pygame.quit()
