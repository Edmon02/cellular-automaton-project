# src/rules.py
"""
High-performance cellular automaton rules engine with vectorized operations.
Optimized for speed using numpy, lookup tables, and efficient algorithms.
"""
import random
import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from enum import IntEnum


class CellType(IntEnum):
    """Cell type enumeration for better type safety."""
    DAY = 0
    NIGHT = 1


class Direction(IntEnum):
    """Direction indices for lookup tables."""
    LEFT_UP = 0      # ↖️
    UP = 1           # ⬆️
    RIGHT_UP = 2     # ↗️
    LEFT = 3         # ⬅️
    RIGHT = 4        # ➡️
    LEFT_DOWN = 5    # ↙️
    DOWN = 6         # ⬇️
    RIGHT_DOWN = 7   # ↘️


@dataclass
class MoveResult:
    """Result of a movement operation."""
    success: bool
    new_x: int
    new_y: int
    additional_toggles: List[Tuple[int, int]]


class OptimizedRules:
    """
    High-performance rules engine using vectorized operations and lookup tables.
    """
    
    def __init__(self):
        # Pre-computed direction vectors for O(1) lookup
        self._direction_vectors = np.array([
            [-1, -1],  # LEFT_UP ↖️
            [0, -1],   # UP ⬆️
            [1, -1],   # RIGHT_UP ↗️
            [-1, 0],   # LEFT ⬅️
            [1, 0],    # RIGHT ➡️
            [-1, 1],   # LEFT_DOWN ↙️
            [0, 1],    # DOWN ⬇️
            [1, 1],    # RIGHT_DOWN ↘️
        ], dtype=np.int8)
        
        # Diagonal directions only (original self.directions)
        self._diagonal_dirs = np.array([0, 2, 5, 7], dtype=np.int8)  # Indices in direction_vectors
        
        # Current directions for each entity type
        self._entity_directions = {
            CellType.NIGHT: 0,  # LEFT_UP
            CellType.DAY: 0     # LEFT_UP
        }
        
        # Boundary reflection lookup table for ultra-fast bounds checking
        self._boundary_reflections = self._create_boundary_lookup()
        
        # Random number generator for deterministic seeding if needed
        self._rng = np.random.default_rng()

    def _create_boundary_lookup(self) -> Dict[Tuple[int, str], int]:
        """Create lookup table for boundary reflections."""
        lookup = {}
        
        # Use integer indices for directions
        LEFT_UP, UP, RIGHT_UP, LEFT, RIGHT, LEFT_DOWN, DOWN, RIGHT_DOWN = range(8)
        
        # Top boundary reflections
        lookup[(LEFT_UP, 'top')] = LEFT_DOWN
        lookup[(RIGHT_UP, 'top')] = RIGHT_DOWN
        
        # Bottom boundary reflections  
        lookup[(LEFT_DOWN, 'bottom')] = LEFT_UP
        lookup[(RIGHT_DOWN, 'bottom')] = RIGHT_UP
        
        # Left boundary reflections
        lookup[(LEFT_UP, 'left')] = RIGHT_UP
        lookup[(LEFT_DOWN, 'left')] = RIGHT_DOWN
        
        # Right boundary reflections
        lookup[(RIGHT_UP, 'right')] = LEFT_UP
        lookup[(RIGHT_DOWN, 'right')] = LEFT_DOWN
                
        return lookup

    def move_entity(self, entity, grid) -> MoveResult:
        """
        Move an entity using vectorized operations and precise collision detection.
        Returns a MoveResult with success status and additional cells to toggle.
        """
        # Store previous position for debugging
        prev_x, prev_y = entity.x, entity.y
        
        # Get current direction for this entity type
        current_dir = self._entity_directions[entity.type]
        direction_vector = self._direction_vectors[current_dir]
        
        # Calculate new position using vectorized operation
        new_pos = np.array([entity.x, entity.y]) + direction_vector
        new_x, new_y = new_pos
        
        # Ensure coordinates are integers
        new_x, new_y = int(new_x), int(new_y)
        
        # Fast boundary checking with lookup table
        boundary_hit = self._check_boundaries(new_x, new_y, grid.width, grid.height)
        if boundary_hit:
            # Update direction using lookup table
            self._entity_directions[entity.type] = self._get_boundary_reflection(
                current_dir, boundary_hit, new_x, new_y, grid.width, grid.height
            )
            # Recursive call with new direction (tail recursion could be optimized)
            return self.move_entity(entity, grid)
        
        # Precise collision detection: check if new position has same cell type
        cell_at_new_pos = grid.get_state(new_x, new_y)
        if cell_at_new_pos == entity.type:
            # Handle collision and get additional cells to toggle
            new_direction, additional_cells = self._handle_collision(
                entity, new_x, new_y, grid
            )
            self._entity_directions[entity.type] = new_direction
            
            # Apply the collision toggle at the EXACT collision point
            grid.toggle_cell(new_x, new_y)
            collision_toggles = [(new_x, new_y)]
            
            # Get additional collision-based toggles
            extra_toggles = self._get_collision_toggles(new_x, new_y, additional_cells, grid)
            collision_toggles.extend(extra_toggles)
            
            # Recursive move with new direction
            result = self.move_entity(entity, grid)
            result.additional_toggles.extend(collision_toggles)
            
            return result
        
        # Successful move - update entity position
        entity.px, entity.py = entity.x, entity.y  # Store previous position
        entity.x, entity.y = new_x, new_y
        
        return MoveResult(
            success=True,
            new_x=new_x,
            new_y=new_y,
            additional_toggles=[]
        )

    def _check_boundaries(self, x: int, y: int, width: int, height: int) -> Optional[str]:
        """Fast boundary checking using comparison operations."""
        if y < 0:
            return 'top'
        elif y >= height:
            return 'bottom'
        elif x < 0:
            return 'left'
        elif x >= width:
            return 'right'
        return None

    def _get_boundary_reflection(self, direction: int, boundary: str, 
                               x: int, y: int, width: int, height: int) -> int:
        """Get reflected direction using lookup table."""
        return self._boundary_reflections.get((direction, boundary), direction)

    def _handle_collision(self, entity, x: int, y: int, grid) -> Tuple[int, List[int]]:
        """
        Handle collision with same cell type using optimized lookup.
        Returns new direction and list of additional cells to toggle.
        """
        current_dir = self._entity_directions[entity.type]
        
        # Get potential alternative directions
        alternatives = self._get_collision_alternatives(current_dir)
        
        # Vectorized collision checking
        for alt_dir in alternatives:
            alt_vector = self._direction_vectors[alt_dir]
            test_pos = np.array([entity.x, entity.y]) + alt_vector
            test_x, test_y = test_pos
            
            # Check bounds and cell state
            if (0 <= test_x < grid.width and 0 <= test_y < grid.height and
                grid.get_state(test_x, test_y) != entity.type):
                return alt_dir, self._get_additional_cells_for_direction(alt_dir)
        
        # If no alternative found, choose random direction
        random_dir = self._rng.choice(self._diagonal_dirs)
        return random_dir, self._get_multiple_additional_cells(current_dir)

    def _get_collision_alternatives(self, direction: int) -> List[int]:
        """Get alternative directions for collision handling."""
        # Use integer constants for directions
        LEFT_UP, UP, RIGHT_UP, LEFT, RIGHT, LEFT_DOWN, DOWN, RIGHT_DOWN = range(8)
        
        alternatives_map = {
            LEFT_UP: [RIGHT_UP, LEFT_DOWN],      # 0: [2, 5]
            RIGHT_UP: [LEFT_UP, RIGHT_DOWN],     # 2: [0, 7]
            LEFT_DOWN: [LEFT_UP, RIGHT_DOWN],    # 5: [0, 7]
            RIGHT_DOWN: [RIGHT_UP, LEFT_DOWN]    # 7: [2, 5]
        }
        return alternatives_map.get(direction, [])

    def _get_additional_cells_for_direction(self, direction: int) -> List[int]:
        """Get additional cells to toggle based on direction."""
        # Use integer constants for directions
        LEFT_UP, UP, RIGHT_UP, LEFT, RIGHT, LEFT_DOWN, DOWN, RIGHT_DOWN = range(8)
        
        additional_map = {
            RIGHT_UP: [LEFT],      # 2: [3]
            LEFT_DOWN: [RIGHT],    # 5: [4]
            LEFT_UP: [RIGHT],      # 0: [4]
            RIGHT_DOWN: [UP]       # 7: [1]
        }
        return additional_map.get(direction, [])

    def _get_multiple_additional_cells(self, direction: int) -> List[int]:
        """Get multiple additional cells for random direction changes."""
        # Use integer constants for directions
        LEFT_UP, UP, RIGHT_UP, LEFT, RIGHT, LEFT_DOWN, DOWN, RIGHT_DOWN = range(8)
        
        multiple_map = {
            LEFT_UP: [RIGHT, LEFT],        # 0: [4, 3]
            RIGHT_UP: [LEFT, DOWN],        # 2: [3, 6]
            LEFT_DOWN: [RIGHT, DOWN],      # 5: [4, 6]
            RIGHT_DOWN: [UP, LEFT]         # 7: [1, 3]
        }
        return multiple_map.get(direction, [])

    def _get_collision_toggles(self, x: int, y: int, additional_cells: List[int], 
                             grid) -> List[Tuple[int, int]]:
        """Calculate collision-based cell toggles using precise coordinate validation."""
        return self._get_precise_collision_toggles(x, y, additional_cells, grid)

    def update_counts_vectorized(self, grid) -> Tuple[int, int]:
        """
        Ultra-fast count update using numpy vectorized operations.
        ~100x faster than loops for large grids.
        """
        night_count = np.sum(grid.cells)
        day_count = grid.cells.size - night_count
        return day_count, night_count

    def batch_move_entities(self, entities: List, grid) -> List[Tuple[int, int]]:
        """
        Move multiple entities in batch for maximum performance.
        Returns list of all cells that need to be toggled.
        """
        all_toggles = []
        
        for entity in entities:
            result = self.move_entity(entity, grid)
            if result.success:
                all_toggles.extend(result.additional_toggles)
        
        return all_toggles

    def apply_toggles_vectorized(self, grid, toggles: List[Tuple[int, int]]) -> None:
        """Apply multiple cell toggles using vectorized operations."""
        if not toggles:
            return
        
        # Convert to numpy arrays for vectorized operations
        positions = np.array(toggles)
        x_coords = positions[:, 0]
        y_coords = positions[:, 1]
        
        # Vectorized toggle operation
        grid.cells[y_coords, x_coords] = 1 - grid.cells[y_coords, x_coords]

    def _validate_coordinates(self, x: int, y: int, grid) -> bool:
        """Validate that coordinates are within grid bounds."""
        return 0 <= x < grid.width and 0 <= y < grid.height
    
    def _get_precise_collision_toggles(self, collision_x: int, collision_y: int, 
                                     additional_cells: List[int], grid) -> List[Tuple[int, int]]:
        """
        Calculate precise collision-based cell toggles with coordinate validation.
        Only toggles cells that are actually adjacent to the collision point.
        """
        if not additional_cells:
            return []
        
        # Ensure collision point is valid
        if not self._validate_coordinates(collision_x, collision_y, grid):
            return []
        
        # Calculate additional positions relative to collision point
        additional_vectors = self._direction_vectors[additional_cells]
        base_pos = np.array([collision_x, collision_y])
        additional_positions = base_pos + additional_vectors
        
        # Filter valid positions and ensure they're integers
        valid_toggles = []
        for pos in additional_positions:
            pos_x, pos_y = int(pos[0]), int(pos[1])
            if self._validate_coordinates(pos_x, pos_y, grid):
                valid_toggles.append((pos_x, pos_y))
        
        return valid_toggles

    def move_entity_debug(self, entity, grid) -> Tuple[MoveResult, Dict]:
        """
        Debug version of move_entity that provides detailed coordinate information.
        """
        debug_info = {
            'initial_pos': (entity.x, entity.y),
            'entity_type': entity.type,
            'direction': self._entity_directions[entity.type],
            'grid_state_at_pos': grid.get_state(entity.x, entity.y),
            'collisions': [],
            'boundary_hits': [],
            'final_pos': None
        }
        
        result = self.move_entity(entity, grid)
        debug_info['final_pos'] = (entity.x, entity.y)
        
        return result, debug_info
