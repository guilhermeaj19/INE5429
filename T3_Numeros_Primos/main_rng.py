import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from rng_algorithm import RNGAlgorithm
from inversive_congruential_generator import InversiveCongruentialGenerator
from blum_blum_shub import BlumBlumShub


#Funcao auxiliar para o Blum Blum Shib
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
    p = prev_bbs_usable_prime(2**(n_bits//2) - 1) #n_bits//2 para que m nao ultrapasse n_bits
    q = prev_bbs_usable_prime(p)
    m = p*q
    seed = m//2
    return (seed, m)

# Roda n_numbers de um algoritmo RNG para cada n_bits dado. Retorna o tempo médio para cada tamanho (em ms)
def test_rng_algorithm(rng_algortihm: RNGAlgorithm, args_definer: "function", lengths_bits: list[int], n_numbers: int) -> list[float]:
    times = []
    print(f"{'N bits':<8} | {'Time (ms)':<15}") # Cria a tabela que é vista no relatório
    print(f"{'-'*8}-|{'-'*15}")
    for n_bits in lengths_bits:
        rng = rng_algortihm(*args_definer(n_bits))
        sum_time_ns = 0
        for _ in range(n_numbers):
            start = time.process_time_ns()
            rng.generate()
            end = time.process_time_ns()
            sum_time_ns += (end - start)
        avg_time_ms = sum_time_ns / (1e6 * n_numbers)
        times.append(avg_time_ms)
        print(f"{n_bits:<8} | {avg_time_ms:<10}") # Parte da tabela

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

    # Cria o gráfico que é visto no relatório
    plt.xscale("log")
    plt.xlabel("Number of bits")
    plt.ylabel("Time (ms)")

    for algorithm, times in rng_times.items():
        plt.scatter(lengths, times, label=algorithm)
        z = np.polyfit(lengths, times, 1)
        p = np.poly1d(z)
        plt.plot(lengths, p(lengths), "--")

    plt.legend()
    plt.savefig("plot_execution_times_rng")
    plt.show()
    
    