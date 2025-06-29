# src/main.py
from simulation import Simulation
from visualization import Visualizer
import pygame


def main():
    # Grid size (e.g., 20x20 cells)
    sim = Simulation(20, 20)
    # Enable grid lines and coordinates for debugging
    viz = Visualizer(sim, cell_size=25, show_grid=True, show_coordinates=False)

    running = True
    clock = pygame.time.Clock()
    step_count = 0
    debug_mode = False  # Set to True for debugging

    print("🎯 Cellular Automaton with Optimized Rules")
    print("Press 'D' to toggle debug mode")
    print("Press 'G' to toggle grid lines")
    print("Press 'C' to toggle coordinate labels")
    print("Press 'R' to reset simulation")
    print("Press 'O' to switch to optimized step")
    print("-" * 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    debug_mode = not debug_mode
                    print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
                elif event.key == pygame.K_g:
                    viz.show_grid = not viz.show_grid
                    print(f"Grid lines: {'ON' if viz.show_grid else 'OFF'}")
                elif event.key == pygame.K_c:
                    viz.show_coordinates = not viz.show_coordinates
                    print(f"Coordinate labels: {'ON' if viz.show_coordinates else 'OFF'}")
                elif event.key == pygame.K_r:
                    sim = Simulation(20, 20)
                    step_count = 0
                    print("Simulation reset")
                elif event.key == pygame.K_o:
                    print("Switching to optimized step mode")

        # Run simulation step with optional debugging
        if debug_mode and step_count % 30 == 0:  # Debug every 30 frames
            print(f"\nStep {step_count}:")
            print(f"Entity positions: {[(e.x, e.y, e.type) for e in sim.entities]}")
            print(f"Counts - Day: {sim.day_count}, Night: {sim.night_count}")
        
        # Use optimized step for better performance
        sim.step_optimized()
        viz.draw()  # Update the display
        
        clock.tick(10)  # Limit to 100 FPS for smooth animation
        step_count += 1

    viz.close()


if __name__ == "__main__":
    main()
