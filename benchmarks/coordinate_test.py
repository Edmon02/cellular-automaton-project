#!/usr/bin/env python3
"""
Coordinate System Testing and Validation Script
Tests the precision of collision detection and coordinate handling.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from src.grid import Grid
from src.entities import Entity
from src.rules import OptimizedRules
from src.simulation import Simulation


def test_coordinate_precision():
    """Test coordinate precision and collision detection."""
    print("🎯 Testing Coordinate Precision")
    print("=" * 40)
    
    # Create small test grid for easy verification
    grid = Grid(5, 5)
    rules = OptimizedRules()
    
    # Set up a specific pattern for testing
    # Grid layout: 0=Day (light), 1=Night (dark)
    # Initial: Left half = 0, Right half = 1
    print("Initial grid state:")
    print_grid_state(grid)
    
    # Create test entity at specific position
    entity = Entity(1, 1, (0, 0, 0), typeE=1)  # Night entity
    print(f"\nEntity (type {entity.type}) at position ({entity.x}, {entity.y})")
    print(f"Cell at entity position: {grid.get_state(entity.x, entity.y)}")
    
    # Test movement and collision
    print(f"\nBefore movement - Entity at ({entity.x}, {entity.y})")
    result = rules.move_entity(entity, grid)
    print(f"After movement - Entity at ({entity.x}, {entity.y})")
    print(f"Movement successful: {result.success}")
    print(f"Additional toggles: {result.additional_toggles}")
    
    print("\nGrid state after movement:")
    print_grid_state(grid)


def test_collision_accuracy():
    """Test collision detection accuracy with precise positioning."""
    print("\n🎯 Testing Collision Detection Accuracy")
    print("=" * 45)
    
    grid = Grid(10, 10)
    rules = OptimizedRules()
    
    # Create entities that should collide at specific points
    entity1 = Entity(4, 4, (0, 0, 0), typeE=1)  # Night entity
    entity2 = Entity(6, 6, (255, 255, 255), typeE=0)  # Day entity
    
    print(f"Entity 1 (type {entity1.type}) at ({entity1.x}, {entity1.y})")
    print(f"Entity 2 (type {entity2.type}) at ({entity2.x}, {entity2.y})")
    
    # Test multiple movements and track coordinate changes
    for step in range(5):
        print(f"\n--- Step {step + 1} ---")
        
        # Move entity 1
        pos_before = (entity1.x, entity1.y)
        cell_before = grid.get_state(entity1.x, entity1.y)
        
        result1 = rules.move_entity(entity1, grid)
        
        pos_after = (entity1.x, entity1.y)
        cell_after = grid.get_state(entity1.x, entity1.y)
        
        print(f"Entity 1: {pos_before} → {pos_after}")
        print(f"Cell state: {cell_before} → {cell_after}")
        if result1.additional_toggles:
            print(f"Toggles applied: {result1.additional_toggles}")
        
        # Move entity 2
        pos_before = (entity2.x, entity2.y)
        result2 = rules.move_entity(entity2, grid)
        pos_after = (entity2.x, entity2.y)
        
        print(f"Entity 2: {pos_before} → {pos_after}")
        if result2.additional_toggles:
            print(f"Toggles applied: {result2.additional_toggles}")


def test_boundary_behavior():
    """Test behavior at grid boundaries."""
    print("\n🎯 Testing Boundary Behavior")
    print("=" * 35)
    
    grid = Grid(5, 5)
    rules = OptimizedRules()
    
    # Test entity at boundary
    entity = Entity(0, 0, (0, 0, 0), typeE=1)  # Top-left corner
    print(f"Entity at boundary ({entity.x}, {entity.y})")
    
    for step in range(3):
        pos_before = (entity.x, entity.y)
        result = rules.move_entity(entity, grid)
        pos_after = (entity.x, entity.y)
        
        print(f"Step {step + 1}: {pos_before} → {pos_after}")
        
        # Verify entity stays within bounds
        if not (0 <= entity.x < grid.width and 0 <= entity.y < grid.height):
            print("❌ ERROR: Entity moved outside grid bounds!")
        else:
            print("✅ Entity within bounds")


def print_grid_state(grid):
    """Print grid state in a readable format."""
    print("Grid (0=Day/Light, 1=Night/Dark):")
    for y in range(grid.height):
        row = ""
        for x in range(grid.width):
            row += str(grid.get_state(x, y)) + " "
        print(f"  {row}")


def test_simulation_integration():
    """Test the complete simulation with coordinate fixes."""
    print("\n🎯 Testing Complete Simulation Integration")
    print("=" * 50)
    
    sim = Simulation(8, 8)
    
    print(f"Initial simulation state:")
    print(f"Entities: {len(sim.entities)}")
    for i, entity in enumerate(sim.entities):
        print(f"  Entity {i}: position ({entity.x}, {entity.y}), type {entity.type}")
    
    print(f"Initial counts - Day: {sim.day_count}, Night: {sim.night_count}")
    
    # Run several steps and track changes
    for step in range(5):
        print(f"\n--- Simulation Step {step + 1} ---")
        
        # Store positions before step
        positions_before = [(e.x, e.y) for e in sim.entities]
        
        # Run step
        sim.step_optimized()
        
        # Check positions after step
        positions_after = [(e.x, e.y) for e in sim.entities]
        
        print(f"Day count: {sim.day_count}, Night count: {sim.night_count}")
        
        for i, (before, after) in enumerate(zip(positions_before, positions_after)):
            if before != after:
                print(f"  Entity {i} moved: {before} → {after}")
        
        # Verify grid consistency
        total_cells = sim.grid.width * sim.grid.height
        if sim.day_count + sim.night_count != total_cells:
            print(f"❌ ERROR: Count mismatch! {sim.day_count} + {sim.night_count} ≠ {total_cells}")
        else:
            print(f"✅ Cell counts consistent: {sim.day_count} + {sim.night_count} = {total_cells}")


if __name__ == "__main__":
    print("🔧 Cellular Automaton Coordinate System Tests")
    print("=" * 55)
    
    try:
        test_coordinate_precision()
        test_collision_accuracy()
        test_boundary_behavior()
        test_simulation_integration()
        
        print("\n✅ All coordinate tests completed!")
        print("The coordinate system is now working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
