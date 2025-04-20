import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from rng_algorithm import RNGAlgorithm
from inversive_congruential_generator import InversiveCongruentialGenerator
from blum_blum_shub import BlumBlumShub


#Helper function to Blum Blum Shib algortihm
def prev_bbs_usable_prime(x: int) -> int:
        p = sp.prevprime(x)
        while (p % 4 != 3):
            p = sp.prevprime(p)
        return p

def inversive_congruential_generator_args(n_bits: int) -> tuple[int,int,int,int]:
    m = sp.prevprime(2**(n_bits) - 1)
    seed = m//2
    a = 5520335699031059059 % m
    b = 2752743153957480735 % m
    return (seed, a, b, m)

def blum_blum_shib_args(n_bits: int) -> tuple[int,int]:
    p = prev_bbs_usable_prime(2**(n_bits//2) - 1) #n_bits//2 because the m cant pass n_bits
    q = prev_bbs_usable_prime(p)
    m = p*q
    seed = m//2
    return (seed, m)

# Run n_numbers of a RNG Algorithm for each n_bits given. Returns the average time for each length (in milliseconds).
def test_rng_algorithm(rng_algortihm: RNGAlgorithm, args_definer: "function", lengths_bits: list[int], n_numbers: int) -> list[float]:
    times = []
    print("N bits\t| Time (ms)")
    print("---------------------")
    for n_bits in lengths_bits:
        rng = rng_algortihm(*args_definer(n_bits))
        sum = 0
        # sum_n_bits = 0
        for i in range(n_numbers):
            start = time.process_time_ns()
            number = rng.generate()
            end = time.process_time_ns()
            # sum_n_bits += number.bit_length()
            sum += (end-start)
        times.append(sum/(1e6*n_numbers))
        print(f"{n_bits}\t| {times[-1]}")
        # print(f"Execution time for {n_numbers} number with {n_bits} bits: {times[-1]} ms")
        # print(f"Average number of bits for {n_bits} bits: {sum_n_bits/n_numbers:.2f} bits\n")
    
    return times

if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    lengths = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    n_numbers = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    rng_times = dict()

    print(f"Testing Blum Blum Shub for {n_numbers} numbers\n")
    
    rng_times["Blum Blum Shub"] = test_rng_algorithm(BlumBlumShub, blum_blum_shib_args, lengths, n_numbers)

    print(f"\nTesting Inversive Congruential Generator for {n_numbers} numbers\n")
    rng_times["Inversive Congruential Generator"] = test_rng_algorithm(InversiveCongruentialGenerator, inversive_congruential_generator_args, lengths, n_numbers)

    plt.xscale("log")
    plt.xlabel("Number of bits")
    plt.ylabel("Time (ms)")
    lines = []
    for times in rng_times.values():

        plt.scatter(lengths, times)
        z = np.polyfit(lengths, times, 1)
        p = np.poly1d(z)
        lines.append(plt.plot(lengths,p(lengths),"--")[0])
        plt.plot(lengths, times, "o")
    plt.legend(lines, rng_times.keys())
    plt.savefig("plot_execution_times")
    plt.show()
    
    