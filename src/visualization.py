# src/visualization.py
import pygame


class Visualizer:
    def __init__(self, simulation, cell_size=20):
        self.simulation = simulation
        self.cell_size = cell_size
        self.width = simulation.grid.width * cell_size
        self.height = simulation.grid.height * cell_size
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height + 30)
        )  # Extra space for text
        pygame.display.set_caption("Cellular Automaton Simulation")
        self.font = pygame.font.SysFont(None, 24)

    def draw(self):
        self.screen.fill((200, 200, 200))  # Background

        # Draw split-screen background
        for y in range(self.simulation.grid.height):
            for x in range(self.simulation.grid.width):
                color = (
                    (17, 74, 88)
                    if self.simulation.grid.get_state(x, y) == 0
                    else (216, 231, 226)
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
