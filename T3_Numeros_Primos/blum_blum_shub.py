import sys
import sympy
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import time
import random
from helper import dec2bin
#https://asecuritysite.com/encryption/blum
def prev_usable_prime(x):
        p = sympy.nextprime(x)
        while (p % 4 != 3):
            p = sympy.nextprime(p)
        return p

class BlumBlumShub:
    def __init__(self, seed, m):
        self.__seed = seed
        self.__M = m
        self.__x = self.__seed
    
    def reset(self) -> None:
        self.__x = self.__seed
        
    def generate(self) -> int:
        self.__x = self.__x*self.__x % self.__M
        return self.__x

if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    lengths = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    times = []
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    for n_bits in lengths:
        p = prev_usable_prime(2**(n_bits-1)-1)
        q = prev_usable_prime(p)
        m = p*q
        rng = BlumBlumShub(random.randint(0, m), m)
        sum = 0
        sum_n_bits = 0
        for i in range(n):
            start = dt.datetime.now()
            number = rng.generate()
            end = dt.datetime.now()
            sum_n_bits += len(dec2bin(number))
            time.sleep(0.0005)
            sum += (end.microsecond-start.microsecond)
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