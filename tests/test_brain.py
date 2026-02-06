import unittest
import numpy as np
from src.config import Config
from src.brain import Brain
from src.entity import Entity
from src.world import World
from src.genome import Genome

class TestBrain(unittest.TestCase):
    def test_brain_initialization(self):
        # Create a genome with known values
        # INPUT=5, HIDDEN=8, OUTPUT=2
        # Length = 5*8 + 8*2 = 40 + 16 = 56
        length = Config.GENOME_LENGTH
        genes = np.zeros(length)
        # Set first weight to 1.0 (mapped to 1.0 -> (1.0*2)-1 = 1.0)
        # Set second weight to 0.0 (mapped to -1.0)
        genes[0] = 1.0
        genes[1] = 0.0

        brain = Brain(genes)

        self.assertEqual(brain.w1.shape, (Config.INPUT_SIZE, Config.HIDDEN_SIZE))
        self.assertEqual(brain.w2.shape, (Config.HIDDEN_SIZE, Config.OUTPUT_SIZE))

        # Check mapped values
        self.assertAlmostEqual(brain.w1[0, 0], 1.0)
        self.assertAlmostEqual(brain.w1[0, 1], -1.0)

    def test_forward_pass(self):
        length = Config.GENOME_LENGTH
        genes = np.random.uniform(0, 1, length)
        brain = Brain(genes)
        inputs = np.zeros(Config.INPUT_SIZE)

        output = brain.forward(inputs)
        self.assertEqual(output.shape, (Config.OUTPUT_SIZE,))
        # Tanh output range [-1, 1]
        self.assertTrue(np.all(output >= -1.0))
        self.assertTrue(np.all(output <= 1.0))

class TestEntityBrainIntegration(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.genome = Genome(Config.GENOME_LENGTH)
        self.entity = Entity(10, 10, self.genome)
        self.world.entities.append(self.entity)

    def test_vision_no_food(self):
        inputs = self.entity.get_inputs(self.world)
        # Vision DX, DY should be 0
        self.assertEqual(inputs[2], 0.0)
        self.assertEqual(inputs[3], 0.0)

    def test_vision_with_food(self):
        # Place food at (15, 10) -> DX=5, DY=0
        self.world.place_food(15, 10)
        inputs = self.entity.get_inputs(self.world)

        # Check normalized vision
        expected_dx = 5.0 / Config.VISION_RADIUS
        self.assertAlmostEqual(inputs[2], expected_dx)
        self.assertEqual(inputs[3], 0.0)

    def test_eating_removes_from_list(self):
        self.world.place_food(11, 10)
        self.assertIn((11, 10), self.world.food_list)

        # Force move to food
        self.entity.move(1, 0, self.world)

        # Check food is gone from grid and list
        self.assertEqual(self.world.grid[10, 11], Config.CELL_EMPTY)
        self.assertNotIn((11, 10), self.world.food_list)

if __name__ == '__main__':
    unittest.main()
