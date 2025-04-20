from rng_algorithm import RNGAlgorithm

#https://asecuritysite.com/encryption/blum
class BlumBlumShub(RNGAlgorithm):
    def __init__(self, seed: int, m: int):
        super().__init__(seed)
        self.M = m
            
    def generate(self) -> int:
        self.x = self.x*self.x % self.M
        return self.x
