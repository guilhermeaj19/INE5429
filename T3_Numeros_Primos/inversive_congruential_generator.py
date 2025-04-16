import sys
import datetime as dt
import time
import matplotlib.pyplot as plt
import numpy as np
import sympy
from random import randint
from helper import dec2bin

#https://www.johndcook.com/blog/2020/02/19/inverse-congruence-rng/
class InversiveCongruentialGenerator:
    def __init__(self, seed, a, c, q):
        self.__seed = seed
        self.__a = a
        self.__c = c
        self.__q = q
        self.__x = self.__seed
    
    def reset(self) -> None:
        self.__x = self.__seed
    
    def generate(self) -> int:
        x_inverse = pow(self.__x, -1, self.__q)
        self.__x = int((self.__a*x_inverse + self.__c)) % self.__q if self.__x != 0 else self.__c
        return self.__x

if __name__ == "__main__":
    sys.setrecursionlimit(100000)

    lengths = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    times = []
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    for n_bits in lengths:
        m = sympy.prevprime(2**(n_bits-1)-1)
        rng = InversiveCongruentialGenerator(randint(0,m), 48271, 2752743153957480735, m)
        sum = 0
        sum_n_bits = 0
        for i in range(n):
            start = dt.datetime.now()
            number = rng.generate()
            end = dt.datetime.now()
            sum_n_bits += len(dec2bin(number))
            time.sleep(0.0005)
            sum += (end.microsecond-start.microsecond)
            # print(len(dec2bin(number)))
        times.append(sum/(1e3*n))
        print(f"Execution time for {n} number with {n_bits} bits: {times[-1]} ms")
        print(f"Average number of bits for {n_bits} bits: {sum_n_bits/n:.2f} bits")

    plt.scatter(lengths, times)
    plt.xscale("log")
    plt.title(f"Average time for generate a random number x number of bits")

    z = np.polyfit(lengths, times, 1)
    p = np.poly1d(z)
    plt.plot(lengths,p(lengths),"b--")
    plt.plot(lengths, times, "ro")

    plt.show()