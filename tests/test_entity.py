import unittest
import numpy as np
from src.config import Config
from src.entity import Entity
from src.genome import Genome
from src.world import World

class TestEntity(unittest.TestCase):
    def setUp(self):
        self.genome = Genome(Config.GENOME_LENGTH)
        # Create a small grid 10x10
        self.grid = np.zeros((10, 10), dtype=np.int8)

    def test_initialization(self):
        entity = Entity(5, 5, self.genome)
        self.assertEqual(entity.position, [5, 5])
        self.assertEqual(entity.energy, Config.STARTING_ENERGY)
        self.assertEqual(entity.age, 0)

    def test_move_valid(self):
        entity = Entity(5, 5, self.genome)
        entity.move(1, 0, self.grid) # Move right
        self.assertEqual(entity.position, [6, 5])

    def test_move_wall_collision(self):
        entity = Entity(5, 5, self.genome)
        self.grid[5, 6] = Config.CELL_WALL # Place wall to the right
        entity.move(1, 0, self.grid)
        self.assertEqual(entity.position, [5, 5]) # Should not move

    def test_move_bounds_collision(self):
        entity = Entity(9, 5, self.genome) # At right edge
        entity.move(1, 0, self.grid)
        self.assertEqual(entity.position, [9, 5]) # Should not move

    def test_eat_food(self):
        entity = Entity(5, 5, self.genome)
        self.grid[5, 6] = Config.CELL_FOOD

        initial_energy = entity.energy
        entity.move(1, 0, self.grid)

        self.assertEqual(entity.position, [6, 5])
        self.assertEqual(entity.energy, initial_energy + Config.ENERGY_FROM_FOOD)
        self.assertEqual(self.grid[5, 6], Config.CELL_EMPTY) # Food consumed

    def test_update_decay(self):
        entity = Entity(5, 5, self.genome)
        initial_energy = entity.energy
        entity.update(self.grid)
        # Energy should decrease by decay amount
        # Note: it might decrease slightly less or more if it found food randomly,
        # but in an empty grid (0s), it won't find food.
        # However, update() calls random move, which might hit bounds.
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
