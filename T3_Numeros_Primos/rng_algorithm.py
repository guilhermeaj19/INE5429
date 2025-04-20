from abc import ABC, abstractmethod

class RNGAlgorithm(ABC):

    def __init__(self, seed: int, *args):
        self.seed = seed
        self.x = self.seed

    @abstractmethod
    def generate(self):
        pass

    def reset(self):
        self.__x = self.__seed