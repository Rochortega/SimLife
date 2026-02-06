import unittest
import pygame
from src.ui import Slider
from src.world import World
from src.config import Config

class TestUI(unittest.TestCase):
    def setUp(self):
        pygame.init() # Needed for font

    def test_slider_initialization(self):
        slider = Slider(10, 10, 100, 20, 0, 10, 5, "Test")
        self.assertEqual(slider.get_value(), 5)
        self.assertEqual(slider.min_val, 0)
        self.assertEqual(slider.max_val, 10)

    def test_slider_update(self):
        slider = Slider(0, 0, 100, 20, 0, 100, 0, "Test")
        # Simulate updating value at pixel 50 (midpoint)
        slider.update_value(50)
        self.assertAlmostEqual(slider.get_value(), 50, delta=1)

        # Simulate out of bounds
        slider.update_value(150)
        self.assertEqual(slider.get_value(), 100)

        slider.update_value(-10)
        self.assertEqual(slider.get_value(), 0)

class TestWorldInteraction(unittest.TestCase):
    def test_clear_grid(self):
        world = World()
        world.place_wall(5, 5)
        self.assertEqual(world.grid[5, 5], Config.CELL_WALL)

        world.clear_grid()
        self.assertEqual(world.grid[5, 5], Config.CELL_EMPTY)

    def test_place_methods(self):
        world = World()
        world.place_wall(1, 1)
        self.assertEqual(world.grid[1, 1], Config.CELL_WALL)

        world.place_food(2, 2)
        self.assertEqual(world.grid[2, 2], Config.CELL_FOOD)

        # Out of bounds should not crash
        try:
            world.place_wall(-1, -1)
            world.place_wall(10000, 10000)
        except IndexError:
            self.fail("place_wall raised IndexError on bounds check")

if __name__ == '__main__':
    unittest.main()
