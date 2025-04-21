import random
import numpy as np
import sympy
import matplotlib.pyplot as plt

from time import process_time_ns
from main_rng import blum_blum_shib_args
from blum_blum_shub import BlumBlumShub
from rng_algorithm import RNGAlgorithm

#Source: https://en.wikipedia.org/wiki/Solovay%E2%80%93Strassen_primality_test
def solovay_strassen(n: int, t: int = 20) -> bool:
    # Testes base
    if n <= 1: return False 
    if n <= 3: return True # 2 ou 3 é primo
    if n % 2 == 0: return False # par, exceto o 2, nunca é primo

    # Realiza o teste t vezes de forma a aumentar a sua confiança
    # No caso de 20 tentativas: 1 - (1/4)^k = 0,999999999999091
    for _ in range(t):
        a = random.randrange(2,n) #Número aleatório entre 2 e n-1

        x = sympy.jacobi_symbol(a,n)

        if x == 0 or pow(a, (n-1)//2, n) != x % n:
            return False
    return True

#Source: https://www.geeksforgeeks.org/python-program-to-check-whether-a-number-is-prime-or-not/
def miller_rabin(n: int, t: int = 20) -> bool:
    if n <= 1: return False
    if n <= 3: return True # 2 ou 3 é primo
    if n % 2 == 0: return False # par, exceto o 2, nunca é primo

    k = 0
    m = n - 1
    # Determina o valor de m e k
    while m % 2 == 0:
        m //= 2
        k += 1

    # Realiza o teste t vezes de forma a aumentar a sua confiança
    # No caso de 20 tentativas: 1 - (1/4)^k = 0,999999999999091
    for _ in range(t):
        a = random.randrange(2, n - 1) # número aleatório no intervalo [2, n - 2]
        x = pow(a, m, n) # a**m (mod n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(k - 1):
            x = pow(x, 2, n)  # x**2 (mod n)
            if x == n - 1:
                break
        else:
            return False  # n é composto

    return True  # n é provavelmente primo

def find_prime(rng: RNGAlgorithm, test_primality: "function") -> tuple[int, int, float]:
    i = 1
    start = process_time_ns()

    n = rng.generate()
    while not test_primality(n):
        n = rng.generate()
        i += 1

    end = process_time_ns()

    return n, i, (end - start)*1e-6

def print_result_table(lengths: list[int], results: dict[str: list]) -> None:
    print(f"{'Algorithm':<16} || {'n bits':<8} || {'Tries':<8} || {'Time (ms)':<10} || {'Number'}")
    print(f"{'-'*16} || {'-'*8} || {'-'*8} || {'-'*10} || {'-'*35}")

    for alg in results.keys():
        for pos, result in enumerate(results[alg]):
            number_str = str(result["n"])
            if len(number_str) > 30:
                number_str = f"{number_str[:15]}...{number_str[-15:]}"

            if pos == 0:
                print(f"{alg:<16} || {lengths[pos]:<8} || {result['tries']:<8} || {result['time']:<10.3f} || {number_str}")
            else:
                print(f"{'':<16} || {lengths[pos]:<8} || {result['tries']:<8} || {result['time']:<10.3f} || {number_str}")

if __name__ == "__main__":

    lengths = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    test_primality_results = {"Miller-Rabin": [], "Solovay-Strassen": []}
    for n_bits in lengths:
        print(f"Testing for {n_bits}")
        rng = BlumBlumShub(*blum_blum_shib_args(n_bits))
        
        random.seed(46371) # Manter a mesma sequência de números em ambos os testes durante a chamada do random.randrange(a,b)
        n, i, time = find_prime(rng, miller_rabin)
        test_primality_results["Miller-Rabin"].append({"n": n, "tries": i, "time": time})
        print(f"Miller-Rabin found it in {i} tries after {time:.3f} ms")

        rng.reset() # Manter a mesma sequência de valores de n a serem testados
        
        random.seed(46371) #  Manter a mesma sequência de números em ambos os testes durante a chamada do random.randrange(a,b)
        n, i, time = find_prime(rng, solovay_strassen)
        test_primality_results["Solovay-Strassen"].append({"n": n, "tries": i, "time": time})
        print(f"Solovay-Strassen found it in {i} tries after {time:.3f} ms\n")

    print()
    print_result_table(lengths, test_primality_results)

    plt.xscale("log")
    plt.xlabel("Number of bits")
    plt.ylabel("Time (ms)")

    for algorithm, results in test_primality_results.items():
        times = [x["time"] for x in results]
        plt.scatter(lengths, times, label=algorithm)
        z = np.polyfit(lengths, times, 1)
        p = np.poly1d(z)
        plt.plot(lengths, p(lengths), "--") 

    plt.legend()
    plt.savefig("plot_execution_times_primality")
    plt.show()

