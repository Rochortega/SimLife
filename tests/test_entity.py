import unittest
import numpy as np
from src.config import Config
from src.entity import Entity
from src.genome import Genome
from src.world import World

class TestEntity(unittest.TestCase):
    def setUp(self):
        self.genome = Genome(Config.GENOME_LENGTH)
        # Use a real World instance instead of raw grid
        self.world = World()
        # Manually set small size for testing logic if needed, but World defaults to screen size.
        # We can just use the world as is, or manipulate its grid directly.

    def test_initialization(self):
        entity = Entity(5, 5, self.genome)
        self.assertEqual(entity.position, [5, 5])
        self.assertEqual(entity.energy, Config.STARTING_ENERGY)
        self.assertEqual(entity.age, 0)

    def test_move_valid(self):
        entity = Entity(5, 5, self.genome)
        entity.move(1, 0, self.world) # Move right
        self.assertEqual(entity.position, [6, 5])

    def test_move_wall_collision(self):
        entity = Entity(5, 5, self.genome)
        self.world.place_wall(6, 5) # Place wall to the right (x=6, y=5)
        entity.move(1, 0, self.world)
        self.assertEqual(entity.position, [5, 5]) # Should not move

    def test_move_bounds_collision(self):
        # Place entity at edge
        width = self.world.width_cells
        entity = Entity(width - 1, 5, self.genome)
        entity.move(1, 0, self.world)
        self.assertEqual(entity.position, [width - 1, 5]) # Should not move

    def test_eat_food(self):
        entity = Entity(5, 5, self.genome)
        self.world.place_food(6, 5) # Place food at x=6, y=5

        initial_energy = entity.energy
        entity.move(1, 0, self.world)

        self.assertEqual(entity.position, [6, 5])
        self.assertEqual(entity.energy, initial_energy + Config.ENERGY_FROM_FOOD)
        self.assertEqual(self.world.grid[5, 6], Config.CELL_EMPTY) # Food consumed
        self.assertNotIn((6, 5), self.world.food_list) # Removed from list

    def test_update_decay(self):
        entity = Entity(5, 5, self.genome)
        initial_energy = entity.energy
        entity.update(self.world)
        self.assertEqual(entity.energy, initial_energy - Config.ENERGY_DECAY)
        self.assertEqual(entity.age, 1)

class TestWorldEntities(unittest.TestCase):
    def test_spawn_entity(self):
        world = World()
        world.spawn_entity()
        self.assertEqual(len(world.entities), 1)

    def test_spawn_population(self):
        world = World()
        world.spawn_initial_population(10)
        self.assertEqual(len(world.entities), 10)

    def test_entity_death(self):
        world = World()
        world.spawn_entity()
        entity = world.entities[0]
        entity.energy = -10 # Kill it

        world.update()
        self.assertEqual(len(world.entities), 0)

if __name__ == '__main__':
    unittest.main()
