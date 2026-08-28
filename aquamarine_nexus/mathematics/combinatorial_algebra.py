import math

class CombinatorialAlgebraCore:
    @staticmethod
    def subfactorial_derangements(n: int) -> dict:
        """!n = round( n! / e ) for n >= 0"""
        if n < 0:
            raise ValueError("n must be non-negative.")
        if n == 0:
            return {"n": 0, "derangements": 1}
        
        subfact = round(math.factorial(n) / math.e)
        return {"n": n, "derangements_subfactorial": subfact, "prob_derangement": round(subfact / math.factorial(n), 6)}

    @staticmethod
    def bell_number_partitions(n: int) -> dict:
        """B_{n+1} = sum_{k=0}^n binom(n, k) * B_k"""
        if n < 0 or n > 25:
            raise ValueError("n must be between 0 and 25.")
        
        bell = [1]
        for i in range(1, n + 1):
            next_b = sum(math.comb(i - 1, k) * bell[k] for k in range(i))
            bell.append(next_b)
        
        return {"n": n, "bell_number_B_n": bell[n]}

    @staticmethod
    def multinomial_coefficient(counts: list) -> dict:
        """(sum k_i)! / (k_1! * k_2! * ... * k_m!)"""
        if any(x < 0 for x in counts) or not counts:
            raise ValueError("Counts must be positive integers.")
        
        n_total = sum(counts)
        denom = 1
        for x in counts:
            denom *= math.factorial(x)
        
        multinomial = math.factorial(n_total) // denom
        return {"total_N": n_total, "multinomial_coefficient": multinomial}
