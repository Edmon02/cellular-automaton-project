# src/rules.py
import random
import numpy as np


class Rules:
    def __init__(self):

        self.full_directions = [
            (-1, -1),  # left-up ↖️
            (0, -1),  # up ⬆️
            (1, -1),  # right-up ↗️
            (-1, 0),  # left ⬅️
            (1, 0),  # right ➡️
            (-1, 1),  # left-down ↙️
            (0, 1),  # down ⬇️
            (1, 1),  # right-down ↘️
        ]
        self.directions = [
            (-1, -1),  # left-up ↖️
            (1, -1),  # right-up ↗️
            (-1, 1),  # left-down ↙️
            (1, 1),  # right-down ↘️
        ]
        self.additional_cells = []
        # self.direction = random.choice(self.directions)
        self.direction_black = self.directions[0]
        self.direction_white = self.directions[0]
        self.direction = self.directions[0]

    def move_entity(self, entity, grid) -> None:
        """Move an entity randomly."""
        print("Moving direction:", self.direction)
        print("Entity type:", entity.type)
        print("Game board:", grid.cells)
        entity.px, entity.py = entity.x, entity.y
        self.direction = (
            self.direction_black if entity.type == 1 else self.direction_white
        )
        dx, dy = self.direction
        new_x: int = entity.x + dx
        new_y = entity.y + dy
        # Check if the new position is within the grid bounds
        if 0 <= new_x < grid.width and 0 <= new_y < grid.height:
            # if self.check_entity_around(new_x, new_y, entity, grid):
            #     self.move_entity(entity, grid)  # Retry moving in the new direction
            #     # Toggle the cell the entity lands on
            #     grid.toggle_cell(new_x, new_y)
            if grid.get_state(new_x, new_y) == entity.type:
                self.update_direction(new_x, new_y, entity, grid)
                self.move_entity(entity, grid)  # Retry moving in the new direction
                # Toggle the cell the entity lands on
                grid.toggle_cell(new_x, new_y)
                # toggle additional cells
                for cell in self.additional_cells:
                    additional_x = new_x + cell[0]
                    additional_y = new_y + cell[1]
                    if (
                        0 <= additional_x < grid.width
                        and 0 <= additional_y < grid.height
                    ):
                        grid.toggle_cell(additional_x, additional_y)
            else:
                entity.x, entity.y = new_x, new_y
        elif 0 > new_y or new_y >= grid.height:
            self.bounds_chek(new_x, new_y, entity, grid)
            self.move_entity(entity, grid)  # Retry moving in the new direction
        if 0 > new_x or new_x >= grid.width:
            self.bounds_chek(new_x, new_y, entity, grid)
            self.move_entity(entity, grid)  # Retry moving in the new direction

        # Toggle the cell the entity lands on
        # grid.toggle_cell(entity.x, entity.y)

    def check_entity_around(self, new_x, new_y, entity, grid):
        """Check if there are any other cell entities around the current entity."""
        for dx, dy in self.full_directions:
            temp_new_x = new_x + dx
            temp_new_y = new_y + dy
            if 0 <= temp_new_x < grid.width and 0 <= temp_new_y < grid.height:
                if grid.get_state(temp_new_x, temp_new_y) == entity.type:
                    return True
        return False

    def update_counts(self, grid, day_count, night_count):
        """Update day and night counts based on cell states."""
        night_cells = np.sum(grid.cells)
        day_cells = (grid.width * grid.height) - night_cells
        return day_count + day_cells, night_count + night_cells

    def bounds_chek(self, new_x, new_y, entity, grid):
        """Check if the entity is out of bounds and change direction accordingly."""

        if 0 > new_y:
            if self.direction == self.directions[0]:
                self.direction = self.directions[2]  # Change to left-down ↙️
            elif self.direction == self.directions[1]:
                self.direction = self.directions[3]  # Change to right-down ↘️
        if new_y >= grid.width:
            if self.direction == self.directions[2]:
                self.direction = self.directions[0]  # Change to left-up ↖️
            elif self.direction == self.directions[3]:
                self.direction = self.directions[1]  # Change to right-up ↗️

        if 0 > new_x:
            if self.direction == self.directions[0]:
                self.direction = self.directions[1]
            elif self.direction == self.directions[2]:
                self.direction = self.directions[3]
        if new_x >= grid.width:
            if self.direction == self.directions[1]:
                self.direction = self.directions[0]
            elif self.direction == self.directions[3]:
                self.direction = self.directions[2]

        if entity.type == 1:
            self.direction_black = self.direction
        else:
            self.direction_white = self.direction

    def update_direction(self, new_x, new_y, entity, grid):
        """Update the entity's direction based on the current position."""

        if self.direction == self.directions[0]:
            temp_directions = [self.directions[1], self.directions[2]]
            dx, dy = temp_directions[0]
            temp_new_x = entity.x + dx
            temp_new_y = entity.y + dy
            if grid.get_state(temp_new_x, temp_new_y) != entity.type:
                self.direction = temp_directions[0]
                self.additional_cells = [self.full_directions[3]]
            else:
                dx, dy = temp_directions[1]
                temp_new_x = entity.x + dx
                temp_new_y = entity.y + dy
                if grid.get_state(temp_new_x, temp_new_y) != entity.type:
                    self.direction = temp_directions[1]
                    self.additional_cells = [self.full_directions[2]]
                else:
                    self.direction = random.choice(self.directions)
                    self.additional_cells = [
                        self.full_directions[2],
                        self.full_directions[3],
                    ]

        elif self.direction == self.directions[1]:
            temp_directions = [self.directions[0], self.directions[3]]
            dx, dy = temp_directions[0]
            temp_new_x = entity.x + dx
            temp_new_y = entity.y + dy
            if grid.get_state(temp_new_x, temp_new_y) != entity.type:
                self.direction = temp_directions[0]
                self.additional_cells = [self.full_directions[6]]
            else:
                dx, dy = temp_directions[1]
                temp_new_x = entity.x + dx
                temp_new_y = entity.y + dy
                if grid.get_state(temp_new_x, temp_new_y) != entity.type:
                    self.direction = temp_directions[1]
                    self.additional_cells = [self.full_directions[3]]
                else:
                    self.direction = random.choice(self.directions)
                    self.additional_cells = [
                        self.full_directions[3],
                        self.full_directions[6],
                    ]

        elif self.direction == self.directions[2]:
            temp_directions = [self.directions[0], self.directions[3]]
            dx, dy = temp_directions[0]
            temp_new_x = entity.x + dx
            temp_new_y = entity.y + dy
            if grid.get_state(temp_new_x, temp_new_y) != entity.type:
                self.direction = temp_directions[0]
                self.additional_cells = [self.full_directions[4]]
            else:
                dx, dy = temp_directions[1]
                temp_new_x = entity.x + dx
                temp_new_y = entity.y + dy
                if grid.get_state(temp_new_x, temp_new_y) != entity.type:
                    self.direction = temp_directions[1]
                    self.additional_cells = [self.full_directions[6]]
                else:
                    self.direction = random.choice(self.directions)
                    self.additional_cells = [
                        self.full_directions[4],
                        self.full_directions[6],
                    ]

        elif self.direction == self.directions[3]:
            temp_directions = [self.directions[1], self.directions[2]]
            dx, dy = temp_directions[0]
            temp_new_x = entity.x + dx
            temp_new_y = entity.y + dy
            if grid.get_state(temp_new_x, temp_new_y) != entity.type:
                self.direction = temp_directions[0]
                self.additional_cells = [self.full_directions[3]]
            else:
                dx, dy = temp_directions[1]
                temp_new_x = entity.x + dx
                temp_new_y = entity.y + dy
                if grid.get_state(temp_new_x, temp_new_y) != entity.type:
                    self.direction = temp_directions[1]
                    self.additional_cells = [self.full_directions[1]]
                else:
                    self.direction = random.choice(self.directions)
                    self.additional_cells = [
                        self.full_directions[1],
                        self.full_directions[3],
                    ]

        if entity.type == 1:
            self.direction_black = self.direction
        else:
            self.direction_white = self.direction
