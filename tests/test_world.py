import unittest
import numpy as np
from src.config import Config
from src.world import World

class TestWorld(unittest.TestCase):
    def test_grid_initialization(self):
        world = World()
        expected_width = Config.SCREEN_WIDTH // Config.CELL_SIZE
        expected_height = Config.SCREEN_HEIGHT // Config.CELL_SIZE
        self.assertEqual(world.grid.shape, (expected_height, expected_width))
        self.assertTrue(np.all(world.grid == Config.CELL_EMPTY))

    def test_randomize_food(self):
        world = World()
        amount = 50
        world.randomize_food(amount)

        # Count non-zero elements
        food_count = np.sum(world.grid == Config.CELL_FOOD)
        self.assertEqual(food_count, amount)

    def test_no_overwrite_wall(self):
        world = World()
        # Manually set dimensions small for control
        world.width_cells = 10
        world.height_cells = 10
        world.grid = np.zeros((10, 10), dtype=np.int8)

        # Place a "wall" at (0,0)
        world.grid[0, 0] = Config.CELL_WALL

        # Try to place food
        world.randomize_food(10)

        # Check that (0,0) is still a wall
        self.assertEqual(world.grid[0, 0], Config.CELL_WALL)

    def test_draw_logic_data(self):
        world = World()
        world.grid[1, 1] = Config.CELL_FOOD
        world.grid[2, 2] = Config.CELL_WALL

        rows, cols = np.where(world.grid != Config.CELL_EMPTY)
        coords = list(zip(rows, cols))

        self.assertIn((1, 1), coords)
        self.assertIn((2, 2), coords)
        self.assertEqual(len(coords), 2)

if __name__ == '__main__':
    unittest.main()
