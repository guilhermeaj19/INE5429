import sys
import time

class InversiveCongruentialRNG:
    def __init__(self, seed, a, c, q):
        self.__seed = seed
        self.__a = a
        self.__c = c
        self.__q = q
        self.__x = self.__seed
    
    def reset(self):
        self.__x = self.__seed
    
    def generate(self):
        x_inverse = pow(self.__x, -1, self.__q)
        self.__x = int((self.__a*x_inverse + self.__c)) % self.__q if self.__x != 0 else self.__c
        return self.__x

def dec2bin(n):
    if n > 1:
        return str(n % 2) + dec2bin(n//2)
    return str(n % 2)

def discover_q(n_bits, n_numbers = 20, i = 1):
    try:
        print(f"trying 2*{n_bits}-{i}")
        rng = InversiveCongruentialRNG(49283425, 5520335699031059059, 2752743153957480735, 2**(n_bits-1) - i)
        for j in range(n_numbers): rng.generate()
        rng.reset()
        print(f"discovered 2*{n_bits}-{i}")
        return rng
    except ValueError:
        return discover_q(n_bits, n_numbers, i + 1)

if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    n = int(sys.argv[2])
    rng = discover_q(int(sys.argv[1]), n)

    for i in range(n):
        start = time.time()
        number = rng.generate()
        end = time.time()
        print(len(dec2bin(number)))
        print(f"{1000*(end-start):.2f}s")