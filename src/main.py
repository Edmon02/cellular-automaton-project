# src/main.py
from simulation import Simulation
from visualization import Visualizer
import pygame


def main():
    # Grid size (e.g., 20x20 cells)
    sim = Simulation(20, 20)
    viz = Visualizer(sim)

    running = True
    clock = pygame.time.Clock()
    i = 0

    while i != 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sim.step()  # Run one iteration
        viz.draw()  # Update the display
        clock.tick(1)  # Limit to 10 FPS
        i += 1

    viz.close()


if __name__ == "__main__":
    main()
