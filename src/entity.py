import pygame
import random
import numpy as np
from src.config import Config
from src.genome import Genome

class Entity:
    def __init__(self, x: int, y: int, genome: Genome) -> None:
        self.position: list[int] = [x, y]
        self.energy: float = Config.STARTING_ENERGY
        self.age: int = 0
        self.genome: Genome = genome

    def move(self, dx: int, dy: int, world_grid: np.ndarray) -> None:
        """
        Attempts to move the entity by dx, dy.
        Handles collisions with walls and bounds.
        Consumes food if found.
        """
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # Check bounds
        height, width = world_grid.shape
        if not (0 <= new_x < width and 0 <= new_y < height):
            return # Blocked by world bounds

        # Check grid content
        cell_content = world_grid[new_y, new_x]

        if cell_content == Config.CELL_WALL:
            return # Blocked by wall

        # Move is valid, check for food
        if cell_content == Config.CELL_FOOD:
            self.energy += Config.ENERGY_FROM_FOOD
            world_grid[new_y, new_x] = Config.CELL_EMPTY # Eat food

        # Update position
        self.position = [new_x, new_y]

    def update(self, world_grid: np.ndarray) -> None:
        """
        Updates entity state for the current frame.
        """
        self.age += 1
        self.energy -= Config.ENERGY_DECAY

        # Simple random movement for now
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        if dx != 0 or dy != 0:
            self.move(dx, dy, world_grid)

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
