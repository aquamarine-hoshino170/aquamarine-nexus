import math
from aquamarine_nexus.mathematics.basic_algebra import BasicAlgebra

class NumberTheoryCore:
    """Advanced Modular Arithmetic & Multi-Residue Systems"""

    @staticmethod
    def euler_totient(n: int) -> dict:
        """Computes Euler's Totient phi(n) using prime factors"""
        if n <= 0:
            raise ValueError("n must be a positive integer.")
        factors = BasicAlgebra.prime_factorization(n)
        phi = n
        for p in factors.keys():
            phi -= phi // p
        return {"n": n, "totient_phi": phi}

    @staticmethod
    def chinese_remainder_theorem(remainders: list, moduli: list) -> dict:
        """
        Solves system of congruences: x ≡ r_i (mod m_i)
        All moduli must be pairwise coprime.
        """
        if len(remainders) != len(moduli):
            raise ValueError("Remainders and moduli lists must have identical lengths.")
        
        # Total product
        M = 1
        for m in moduli:
            M *= m

        x = 0
        for r_i, m_i in zip(remainders, moduli):
            M_i = M // m_i
            _, inv, _ = BasicAlgebra.extended_gcd(M_i, m_i)
            inv = inv % m_i
            x = (x + r_i * M_i * inv) % M

        return {"solution_x": x, "modulus_M": M}
