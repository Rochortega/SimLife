import pygame
import numpy as np
import random
from src.config import Config
from src.entity import Entity
from src.genome import Genome

class World:
    def __init__(self) -> None:
        self.width_cells: int = Config.SCREEN_WIDTH // Config.CELL_SIZE
        self.height_cells: int = Config.SCREEN_HEIGHT // Config.CELL_SIZE
        # grid shape is (rows, cols) -> (height, width)
        self.grid: np.ndarray = np.zeros((self.height_cells, self.width_cells), dtype=np.int8)
        self.entities: list[Entity] = []
        self.food_list: set[tuple[int, int]] = set()

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
                    self.place_food(x, y)
                    placed = True

                attempts += 1

    def spawn_entity(self, x: int | None = None, y: int | None = None) -> None:
        """
        Spawns a new entity. If x, y are not provided, finds a random empty location.
        """
        if x is None or y is None:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                rx = random.randint(0, self.width_cells - 1)
                ry = random.randint(0, self.height_cells - 1)

                # Check if cell is walkable (not a wall)
                if self.grid[ry, rx] != Config.CELL_WALL:
                    x, y = rx, ry
                    placed = True
                attempts += 1

            if not placed:
                return # Could not find a spot
        else:
            # Bounds check
            if not (0 <= x < self.width_cells and 0 <= y < self.height_cells):
                return
            if self.grid[y, x] == Config.CELL_WALL:
                return

        genome = Genome(Config.GENOME_LENGTH)
        new_entity = Entity(x, y, genome)
        self.entities.append(new_entity)

    def spawn_initial_population(self, amount: int) -> None:
        """
        Spawns the initial population of entities.
        """
        for _ in range(amount):
            self.spawn_entity()

    def update(self) -> None:
        """
        Updates the world state.
        """
        # Update all entities
        active_entities = []
        for entity in self.entities:
            # We pass the full world instance now so Entity can access food_list and remove_food
            entity.update(self)
            if entity.energy > 0:
                active_entities.append(entity)

        self.entities = active_entities

    def clear_grid(self) -> None:
        """
        Clears all walls and food from the grid.
        Entities remain.
        """
        self.grid.fill(Config.CELL_EMPTY)
        self.food_list.clear()

    def place_wall(self, x: int, y: int) -> None:
        """
        Places a wall at grid coordinates if within bounds.
        Removes food if overwriting.
        """
        if 0 <= x < self.width_cells and 0 <= y < self.height_cells:
            # If there was food, remove it from list
            if self.grid[y, x] == Config.CELL_FOOD:
                self.remove_food(x, y)

            self.grid[y, x] = Config.CELL_WALL

    def place_food(self, x: int, y: int) -> None:
        """
        Places food at grid coordinates if within bounds.
        """
        if 0 <= x < self.width_cells and 0 <= y < self.height_cells:
            # If there was a wall, overwrite it.
            # If already food, just ensure it's in list (set handles dups).
            self.grid[y, x] = Config.CELL_FOOD
            self.food_list.add((x, y))

    def remove_food(self, x: int, y: int) -> None:
        """
        Removes food from grid and list.
        """
        # Only act if it IS food (optimization) or just force clear
        if self.grid[y, x] == Config.CELL_FOOD:
            self.grid[y, x] = Config.CELL_EMPTY
            self.food_list.discard((x, y))

    def draw(self, surface: pygame.Surface) -> None:
        """
        Renders the grid to the given surface.
        Optimized to only draw non-empty cells.
        """
        rows, cols = np.where(self.grid != Config.CELL_EMPTY)

        for r, c in zip(rows, cols):
            cell_value: int = self.grid[r, c]

            color: tuple[int, int, int]
            if cell_value == Config.CELL_WALL:
                color = Config.COLOR_WALL
            elif cell_value == Config.CELL_FOOD:
                color = Config.COLOR_FOOD
            else:
                continue

            rect: tuple[int, int, int, int] = (
                c * Config.CELL_SIZE,
                r * Config.CELL_SIZE,
                Config.CELL_SIZE,
                Config.CELL_SIZE
            )
            pygame.draw.rect(surface, color, rect)

        # Draw entities
        for entity in self.entities:
            entity.draw(surface)
