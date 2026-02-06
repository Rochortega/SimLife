import numpy as np

class Genome:
    def __init__(self, length: int) -> None:
        """
        Initializes the genome with random float values between 0.0 and 1.0.
        """
        self.genes: np.ndarray = np.random.uniform(0.0, 1.0, size=length)
