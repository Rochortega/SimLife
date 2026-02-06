import pygame
import random
import numpy as np
import math
from src.config import Config
from src.genome import Genome
from src.brain import Brain

# Type hint for World to avoid circular import issues if checked strictly at runtime,
# but usually we handle this by importing inside methods or using TYPE_CHECKING.
# For simplicity in this script, we assume duck typing or pass 'Any' if needed,
# but python handles this fine at runtime.

class Entity:
    def __init__(self, x: int, y: int, genome: Genome) -> None:
        self.position: list[int] = [x, y]
        self.energy: float = Config.STARTING_ENERGY
        self.age: int = 0
        self.genome: Genome = genome
        self.brain: Brain = Brain(self.genome.genes)

    def get_inputs(self, world) -> np.ndarray:
        """
        Generates input vector for the brain.
        Inputs: [Bias, Energy, Vision_DX, Vision_DY, Random]
        """
        # 1. Bias
        input_bias = 1.0

        # 2. Energy (Normalized 0-1 approx, assuming 100 is max or baseline)
        input_energy = self.energy / 100.0

        # 3. Vision (Find closest food)
        vision_dx = 0.0
        vision_dy = 0.0

        closest_dist_sq = Config.VISION_RADIUS ** 2 + 1 # Initialize larger than max vision

        # Optimization: Iterate only food items?
        # If food_list is huge, this is slow O(N_food).
        # But usually N_food < N_cells_in_radius.
        # User requested filtering.

        cx, cy = self.position

        found_food = False
        best_target = (0, 0)

        # Iterate food list
        for fx, fy in world.food_list:
            dx = fx - cx
            dy = fy - cy

            # Quick bounding box check
            if abs(dx) > Config.VISION_RADIUS or abs(dy) > Config.VISION_RADIUS:
                continue

            dist_sq = dx*dx + dy*dy
            if dist_sq <= Config.VISION_RADIUS**2:
                if dist_sq < closest_dist_sq:
                    closest_dist_sq = dist_sq
                    best_target = (dx, dy)
                    found_food = True

        if found_food:
            # Normalize DX, DY
            vision_dx = best_target[0] / Config.VISION_RADIUS
            vision_dy = best_target[1] / Config.VISION_RADIUS

        # 5. Random Oscillator
        input_random = np.random.randn() # Standard normal

        return np.array([input_bias, input_energy, vision_dx, vision_dy, input_random])

    def move(self, dx: int, dy: int, world) -> None:
        """
        Attempts to move the entity by dx, dy.
        Handles collisions with walls and bounds.
        Consumes food if found.
        """
        if dx == 0 and dy == 0:
            return

        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # Check bounds
        height, width = world.grid.shape
        if not (0 <= new_x < width and 0 <= new_y < height):
            return # Blocked by world bounds

        # Check grid content
        cell_content = world.grid[new_y, new_x]

        if cell_content == Config.CELL_WALL:
            return # Blocked by wall

        # Move is valid, check for food
        if cell_content == Config.CELL_FOOD:
            self.energy += Config.ENERGY_FROM_FOOD
            # Use world method to remove food correctly from list and grid
            world.remove_food(new_x, new_y)

        # Update position
        self.position = [new_x, new_y]

    def update(self, world) -> None:
        """
        Updates entity state for the current frame.
        """
        self.age += 1
        self.energy -= Config.ENERGY_DECAY

        # Brain control
        inputs = self.get_inputs(world)
        outputs = self.brain.forward(inputs)

        # Decode outputs (0: Move X, 1: Move Y)
        out_x = outputs[0]
        out_y = outputs[1]

        dx = 0
        dy = 0

        # Thresholds > 0.5 -> 1, < -0.5 -> -1, else 0
        if out_x > 0.5: dx = 1
        elif out_x < -0.5: dx = -1

        if out_y > 0.5: dy = 1
        elif out_y < -0.5: dy = -1

        self.move(dx, dy, world)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the entity as a circle.
        """
        # Center of the cell
        center_x = self.position[0] * Config.CELL_SIZE + Config.CELL_SIZE // 2
        center_y = self.position[1] * Config.CELL_SIZE + Config.CELL_SIZE // 2
        radius = Config.CELL_SIZE // 2

        pygame.draw.circle(
            surface,
            Config.COLOR_ENTITY,
            (center_x, center_y),
            radius
        )
