import sys

class BlumBlumShub:
    def __init__(self, seed, m):
        self.__seed = seed
        self.__M = m
        self.__x = self.__seed
    
    def generate(self):
        self.__x = self.__x*self.__x % self.__M
        return self.__x

if __name__ == "__main__":
    seed = sys.argv[1] if len(sys.argv) > 1 else 1203132
    m = sys.argv[2] if len(sys.argv) > 2 else 131242
    rng = BlumBlumShub(seed, m)

    for i in range(20):
        print(rng.generate())