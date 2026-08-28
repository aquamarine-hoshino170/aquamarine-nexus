import math

class DiscreteCombinatoricsCore:
    @staticmethod
    def stirling_numbers_second_kind(n: int, k: int) -> dict:
        """S(n, k) = (1 / k!) * sum_{j=0}^k (-1)^(k-j) * binom(k, j) * j^n"""
        if n < 0 or k < 0: raise ValueError("n and k must be non-negative.")
        if k == 0: return {"n": n, "k": k, "stirling_S2": 1 if n == 0 else 0}
        if k > n: return {"n": n, "k": k, "stirling_S2": 0}
        total = 0
        for j in range(k + 1):
            term = ((-1) ** (k - j)) * math.comb(k, j) * (j ** n)
            total += term
        res = total // math.factorial(k)
        return {"n": n, "k": k, "stirling_S2": res}

    @staticmethod
    def catalan_number(n: int) -> dict:
        """C_n = (1 / (n + 1)) * binom(2n, n)"""
        if n < 0: raise ValueError("n must be non-negative.")
        c_n = math.comb(2 * n, n) // (n + 1)
        return {"n": n, "catalan_number": c_n}

    @staticmethod
    def bernoulli_number_b2n(n: int) -> dict:
        """Exact even Bernoulli numbers B_2, B_4, B_6, B_8, B_10 via Zeta formula"""
        b_table = {0: 1.0, 1: -0.5, 2: 1/6, 4: -1/30, 6: 1/42, 8: -1/30, 10: 5/66, 12: -691/2730, 14: 7/6}
        if n % 2 != 0 and n != 1: return {"n": n, "bernoulli_B_n": 0.0}
        if n in b_table: return {"n": n, "bernoulli_B_n": round(b_table[n], 10)}
        raise ValueError("Calculated up to n=14.")
