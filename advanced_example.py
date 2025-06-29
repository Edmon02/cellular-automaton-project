#!/usr/bin/env python3
"""
Advanced usage example for the OptimizedRules system.
Demonstrates professional patterns and high-performance techniques.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
import time
from dataclasses import dataclass
from contextlib import contextmanager

# Import from src directory
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.entities import Entity
from src.grid import Grid
from src.rules import OptimizedRules, CellType, MoveResult


@dataclass
class SimulationStats:
    """Statistics tracking for performance analysis."""
    total_moves: int = 0
    successful_moves: int = 0
    collisions: int = 0
    boundary_hits: int = 0
    toggles_applied: int = 0
    simulation_time: float = 0.0


class AdvancedSimulation:
    """
    Advanced simulation engine using the optimized rules system.
    Demonstrates professional patterns like dependency injection, 
    event handling, and performance monitoring.
    """
    
    def __init__(self, width: int, height: int, rules: Optional[OptimizedRules] = None):
        self.grid = Grid(width, height)
        self.rules = rules or OptimizedRules()
        self.entities: List[Entity] = []
        self.stats = SimulationStats()
        self._event_handlers: Dict[str, List] = {}
        
    def add_entity(self, x: int, y: int, entity_type: CellType) -> Entity:
        """Add an entity with automatic color assignment."""
        color = (0, 0, 0) if entity_type == CellType.NIGHT else (255, 255, 255)
        entity = Entity(x, y, color, typeE=int(entity_type))
        self.entities.append(entity)
        return entity
    
    def add_entities_random(self, count: int, entity_type: Optional[CellType] = None) -> List[Entity]:
        """Add multiple entities at random positions."""
        entities = []
        for _ in range(count):
            x = np.random.randint(0, self.grid.width)
            y = np.random.randint(0, self.grid.height)
            type_to_use = entity_type or np.random.choice(list(CellType))
            entities.append(self.add_entity(x, y, type_to_use))
        return entities
    
    @contextmanager
    def performance_timer(self):
        """Context manager for timing simulation steps."""
        start = time.perf_counter()
        yield
        end = time.perf_counter()
        self.stats.simulation_time += end - start
    
    def step_simulation(self, use_batch: bool = True) -> SimulationStats:
        """
        Execute one simulation step with performance monitoring.
        
        Args:
            use_batch: Whether to use batch operations for maximum performance
        """
        with self.performance_timer():
            if use_batch:
                self._step_batch()
            else:
                self._step_individual()
        
        return self.stats
    
    def _step_batch(self):
        """High-performance batch simulation step."""
        # Batch move all entities
        all_toggles = self.rules.batch_move_entities(self.entities, self.grid)
        
        # Apply all toggles in one vectorized operation
        if all_toggles:
            self.rules.apply_toggles_vectorized(self.grid, all_toggles)
            self.stats.toggles_applied += len(all_toggles)
        
        self.stats.total_moves += len(self.entities)
        self.stats.successful_moves += len(self.entities)  # Simplified for demo
    
    def _step_individual(self):
        """Individual entity processing for comparison."""
        for entity in self.entities:
            result = self.rules.move_entity(entity, self.grid)
            self.stats.total_moves += 1
            
            if result.success:
                self.stats.successful_moves += 1
                if result.additional_toggles:
                    self.rules.apply_toggles_vectorized(self.grid, result.additional_toggles)
                    self.stats.toggles_applied += len(result.additional_toggles)
    
    def run_simulation(self, steps: int, use_batch: bool = True, 
                      print_progress: bool = True) -> SimulationStats:
        """
        Run simulation for specified number of steps.
        
        Args:
            steps: Number of simulation steps
            use_batch: Use batch operations for performance
            print_progress: Print progress information
        """
        if print_progress:
            print(f"🚀 Running {steps} steps with {'batch' if use_batch else 'individual'} processing")
        
        start_time = time.perf_counter()
        
        for step in range(steps):
            self.step_simulation(use_batch)
            
            if print_progress and step % (steps // 10) == 0:
                progress = (step / steps) * 100
                print(f"  Progress: {progress:.1f}% ({step}/{steps})")
        
        total_time = time.perf_counter() - start_time
        
        if print_progress:
            self._print_performance_report(total_time, steps)
        
        return self.stats
    
    def _print_performance_report(self, total_time: float, steps: int):
        """Print detailed performance report."""
        moves_per_second = self.stats.total_moves / total_time
        steps_per_second = steps / total_time
        
        print(f"\n📊 Performance Report:")
        print(f"  Total time: {total_time:.4f}s")
        print(f"  Steps per second: {steps_per_second:.2f}")
        print(f"  Moves per second: {moves_per_second:,.0f}")
        print(f"  Total moves: {self.stats.total_moves:,}")
        print(f"  Successful moves: {self.stats.successful_moves:,}")
        print(f"  Toggles applied: {self.stats.toggles_applied:,}")
        
        # Grid analysis
        day_count, night_count = self.rules.update_counts_vectorized(self.grid)
        total_cells = self.grid.width * self.grid.height
        print(f"  Grid state: {day_count:,} day, {night_count:,} night ({total_cells:,} total)")


def demonstrate_optimization_techniques():
    """Demonstrate advanced optimization techniques."""
    print("\n🔧 Advanced Optimization Techniques Demo")
    print("=" * 50)
    
    # Create test simulation
    sim = AdvancedSimulation(200, 200)
    sim.add_entities_random(100, CellType.NIGHT)
    sim.add_entities_random(100, CellType.DAY)
    
    print(f"Created simulation with {len(sim.entities)} entities on {sim.grid.width}x{sim.grid.height} grid")
    
    # Compare individual vs batch processing
    print("\n1. Individual vs Batch Processing:")
    
    # Test individual processing
    sim_individual = AdvancedSimulation(200, 200)
    sim_individual.entities = [Entity(e.x, e.y, e.color, typeE=e.type) for e in sim.entities]
    
    start = time.perf_counter()
    sim_individual.run_simulation(100, use_batch=False, print_progress=False)
    individual_time = time.perf_counter() - start
    
    # Test batch processing
    sim_batch = AdvancedSimulation(200, 200)
    sim_batch.entities = [Entity(e.x, e.y, e.color, typeE=e.type) for e in sim.entities]
    
    start = time.perf_counter()
    sim_batch.run_simulation(100, use_batch=True, print_progress=False)
    batch_time = time.perf_counter() - start
    
    speedup = individual_time / batch_time
    print(f"  Individual processing: {individual_time:.4f}s")
    print(f"  Batch processing: {batch_time:.4f}s")
    print(f"  Speedup: {speedup:.2f}x")
    
    # Demonstrate vectorized operations
    print("\n2. Vectorized Grid Operations:")
    
    grid = Grid(1000, 1000)
    rules = OptimizedRules()
    
    # Traditional counting (simulated)
    start = time.perf_counter()
    for _ in range(1000):
        # Simulate traditional loop-based counting
        count = 0
        for row in grid.cells:
            for cell in row:
                if cell == 1:
                    count += 1
    traditional_time = time.perf_counter() - start
    
    # Vectorized counting
    start = time.perf_counter()
    for _ in range(1000):
        day_count, night_count = rules.update_counts_vectorized(grid)
    vectorized_time = time.perf_counter() - start
    
    count_speedup = traditional_time / vectorized_time
    print(f"  Traditional counting: {traditional_time:.4f}s")
    print(f"  Vectorized counting: {vectorized_time:.4f}s")
    print(f"  Speedup: {count_speedup:.2f}x")


def memory_efficiency_demo():
    """Demonstrate memory efficiency improvements."""
    print("\n🧠 Memory Efficiency Demo")
    print("=" * 30)
    
    # Compare memory usage of different approaches
    import sys
    
    # Old approach: lists of tuples
    old_directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    old_memory = sys.getsizeof(old_directions) + sum(sys.getsizeof(d) for d in old_directions)
    
    # New approach: numpy arrays
    new_directions = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]], dtype=np.int8)
    new_memory = new_directions.nbytes
    
    print(f"Old approach (list of tuples): {old_memory} bytes")
    print(f"New approach (numpy array): {new_memory} bytes")
    print(f"Memory reduction: {((old_memory - new_memory) / old_memory) * 100:.1f}%")
    
    # Demonstrate lookup table efficiency
    rules = OptimizedRules()
    print(f"Boundary lookup table entries: {len(rules._boundary_reflections)}")
    print(f"Direction vector cache: {rules._direction_vectors.nbytes} bytes")


if __name__ == "__main__":
    print("🎯 Advanced Cellular Automaton Optimization Demo")
    print("=" * 55)
    
    # Main demonstration
    demonstrate_optimization_techniques()
    
    # Memory efficiency
    memory_efficiency_demo()
    
    # Large scale test
    print("\n🚀 Large Scale Performance Test")
    print("=" * 35)
    
    large_sim = AdvancedSimulation(500, 500)
    large_sim.add_entities_random(1000)
    
    print(f"Running large simulation: {large_sim.grid.width}x{large_sim.grid.height} grid, {len(large_sim.entities)} entities")
    
    stats = large_sim.run_simulation(500, use_batch=True)
    
    print(f"\n✅ Demo completed!")
    print(f"   Final performance: {stats.total_moves / large_sim.stats.simulation_time:,.0f} moves/second")
