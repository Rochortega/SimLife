import numpy as np
from src.config import Config

class Brain:
    def __init__(self, genome_genes: np.ndarray) -> None:
        """
        Initializes the neural network weights from the genome genes.
        Decodes genes into w1 and w2 matrices.
        """
        input_size = Config.INPUT_SIZE
        hidden_size = Config.HIDDEN_SIZE
        output_size = Config.OUTPUT_SIZE

        # Calculate split indices
        w1_end = input_size * hidden_size

        # Slice genes
        w1_flat = genome_genes[:w1_end]
        w2_flat = genome_genes[w1_end:]

        # Reshape weights (Input: genes are 0.0-1.0, we shift to -1.0 to 1.0 for weights usually?
        # But genome spec says 0.0-1.0. Let's map 0..1 to -1..1 for better NN performance,
        # or just use 0..1. Standard genetic algos often use -1..1.
        # User requirement says: "Inicializa self.genes... 0.0 y 1.0".
        # I will map them to -1 to 1 for the Brain to allow negative weights.)

        w1_genes = (w1_flat * 2) - 1 # Map [0,1] -> [-1,1]
        w2_genes = (w2_flat * 2) - 1

        self.w1 = w1_genes.reshape((input_size, hidden_size))
        self.w2 = w2_genes.reshape((hidden_size, output_size))

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Performs feed-forward propagation.
        Inputs shape: (INPUT_SIZE,)
        Returns shape: (OUTPUT_SIZE,) values in range [-1, 1] (tanh).
        """
        # Hidden Layer
        # inputs @ w1
        h1 = np.tanh(np.dot(inputs, self.w1))

        # Output Layer
        # h1 @ w2
        output = np.tanh(np.dot(h1, self.w2))

        return output
