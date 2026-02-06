import pygame
import numpy as np
import random
from src.config import Config

class World:
    def __init__(self) -> None:
        self.width_cells: int = Config.SCREEN_WIDTH // Config.CELL_SIZE
        self.height_cells: int = Config.SCREEN_HEIGHT // Config.CELL_SIZE
        # grid shape is (rows, cols) -> (height, width)
        self.grid: np.ndarray = np.zeros((self.height_cells, self.width_cells), dtype=np.int8)

    def randomize_food(self, amount: int) -> None:
        """
        Scatters food randomly in empty cells.
        Ensures we don't overwrite walls or existing food.
        """
        for _ in range(amount):
            placed: bool = False
            attempts: int = 0
            # Try up to 100 times to find an empty cell for this piece of food
            while not placed and attempts < 100:
                x: int = random.randint(0, self.width_cells - 1)
                y: int = random.randint(0, self.height_cells - 1)

                if self.grid[y, x] == Config.CELL_EMPTY:
                    self.grid[y, x] = Config.CELL_FOOD
                    placed = True

                attempts += 1

    def draw(self, surface: pygame.Surface) -> None:
        """
        Renders the grid to the given surface.
        Optimized to only draw non-empty cells.
        """
        # Get coordinates of all non-empty cells
        # rows (y indices), cols (x indices)
        rows, cols = np.where(self.grid != Config.CELL_EMPTY)

        for r, c in zip(rows, cols):
            cell_value: int = self.grid[r, c]

            color: tuple[int, int, int]
            if cell_value == Config.CELL_WALL:
                color = Config.COLOR_WALL
            elif cell_value == Config.CELL_FOOD:
                color = Config.COLOR_FOOD
            else:
                continue # Should not happen given the filter, but safe guard

            rect: tuple[int, int, int, int] = (
                c * Config.CELL_SIZE,
                r * Config.CELL_SIZE,
                Config.CELL_SIZE,
                Config.CELL_SIZE
            )
            pygame.draw.rect(surface, color, rect)
