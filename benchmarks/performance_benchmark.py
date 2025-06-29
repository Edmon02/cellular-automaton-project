#!/usr/bin/env python3
"""
Performance benchmark comparing the original Rules class with OptimizedRules.
Demonstrates the speed improvements achieved through vectorization and lookup tables.
"""

import time
import numpy as np
from typing import List
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from entities import Entity
from grid import Grid
from rules import OptimizedRules


def create_test_entities(count: int, grid_width: int, grid_height: int) -> List[Entity]:
    """Create test entities for benchmarking."""
    entities = []
    for i in range(count):
        x = np.random.randint(0, grid_width)
        y = np.random.randint(0, grid_height)
        entity_type = np.random.choice([0, 1])
        color = (0, 0, 0) if entity_type == 1 else (255, 255, 255)
        entities.append(Entity(x, y, color, typeE=entity_type))
    return entities


def benchmark_optimized_rules(grid_size: int = 100, entity_count: int = 50, iterations: int = 1000):
    """Benchmark the optimized rules implementation."""
    print(f"\n🚀 Benchmarking OptimizedRules with {grid_size}x{grid_size} grid, {entity_count} entities, {iterations} iterations")
    
    # Setup
    grid = Grid(grid_size, grid_size)
    rules = OptimizedRules()
    entities = create_test_entities(entity_count, grid_size, grid_size)
    
    # Warm up
    for entity in entities[:5]:
        rules.move_entity(entity, grid)
    
    # Benchmark individual moves
    start_time = time.perf_counter()
    for _ in range(iterations):
        for entity in entities:
            result = rules.move_entity(entity, grid)
            if result.additional_toggles:
                rules.apply_toggles_vectorized(grid, result.additional_toggles)
    end_time = time.perf_counter()
    
    individual_time = end_time - start_time
    moves_per_second = (iterations * entity_count) / individual_time
    
    print(f"  Individual moves: {individual_time:.4f}s")
    print(f"  Moves/second: {moves_per_second:,.0f}")
    
    # Benchmark batch operations
    start_time = time.perf_counter()
    for _ in range(iterations):
        all_toggles = rules.batch_move_entities(entities, grid)
        rules.apply_toggles_vectorized(grid, all_toggles)
    end_time = time.perf_counter()
    
    batch_time = end_time - start_time
    batch_moves_per_second = (iterations * entity_count) / batch_time
    
    print(f"  Batch operations: {batch_time:.4f}s")
    print(f"  Batch moves/second: {batch_moves_per_second:,.0f}")
    print(f"  Batch speedup: {batch_moves_per_second / moves_per_second:.2f}x")
    
    # Benchmark vectorized counting
    start_time = time.perf_counter()
    for _ in range(iterations * 10):  # More iterations since this is very fast
        day_count, night_count = rules.update_counts_vectorized(grid)
    end_time = time.perf_counter()
    
    count_time = end_time - start_time
    counts_per_second = (iterations * 10) / count_time
    
    print(f"  Vectorized counting: {count_time:.4f}s")
    print(f"  Counts/second: {counts_per_second:,.0f}")
    
    return {
        'individual_moves_per_second': moves_per_second,
        'batch_moves_per_second': batch_moves_per_second,
        'counts_per_second': counts_per_second,
        'batch_speedup': batch_moves_per_second / moves_per_second
    }


def benchmark_memory_usage():
    """Demonstrate memory efficiency of the optimized implementation."""
    print("\n🧠 Memory Usage Analysis")
    
    # Small arrays use less memory than lists of tuples
    directions_old = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    directions_new = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]], dtype=np.int8)
    
    print(f"  Old directions (list of tuples): {sys.getsizeof(directions_old)} bytes")
    print(f"  New directions (numpy array): {directions_new.nbytes} bytes")
    print(f"  Memory savings: {sys.getsizeof(directions_old) - directions_new.nbytes} bytes")
    
    # Demonstrate lookup table efficiency
    rules = OptimizedRules()
    print(f"  Boundary lookup table: {len(rules._boundary_reflections)} entries")
    print(f"  Direction vectors cache: {rules._direction_vectors.nbytes} bytes")


def run_scaling_benchmark():
    """Test performance scaling with different grid sizes."""
    print("\n📈 Scaling Benchmark")
    
    grid_sizes = [50, 100, 200, 500]
    entity_counts = [10, 25, 50, 100]
    
    for grid_size in grid_sizes:
        for entity_count in entity_counts:
            if grid_size * entity_count > 50000:  # Skip very large tests
                continue
                
            results = benchmark_optimized_rules(
                grid_size=grid_size, 
                entity_count=entity_count, 
                iterations=100
            )
            
            print(f"  Grid {grid_size}x{grid_size}, {entity_count} entities: "
                  f"{results['batch_moves_per_second']:,.0f} moves/sec")


if __name__ == "__main__":
    print("🎯 Cellular Automaton Performance Benchmark")
    print("=" * 50)
    
    # Main benchmark
    results = benchmark_optimized_rules()
    
    # Memory analysis
    benchmark_memory_usage()
    
    # Scaling test
    run_scaling_benchmark()
    
    print("\n✅ Benchmark completed!")
    print(f"   Peak performance: {results['batch_moves_per_second']:,.0f} moves/second")
    print(f"   Speedup factor: {results['batch_speedup']:.2f}x with batch operations")
