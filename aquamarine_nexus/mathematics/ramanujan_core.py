import math

class RamanujanMathematicsCore:
    @staticmethod
    def ramanujan_pi_series(terms_k: int = 2) -> dict:
        """1/pi = (2*sqrt(2)/9801) * sum_{k=0}^inf ( (4k)!(1103 + 26390k) / ((k!)^4 * 396^(4k)) )"""
        factor = (2.0 * math.sqrt(2.0)) / 9801.0
        total_sum = 0.0
        for k in range(terms_k):
            num = math.factorial(4 * k) * (1103 + 26390 * k)
            denom = (math.factorial(k) ** 4) * (396 ** (4 * k))
            total_sum += num / denom
        pi_calc = 1.0 / (factor * total_sum)
        return {"terms_evaluated": terms_k, "ramanujan_pi": f"{pi_calc:.15f}", "error": f"{abs(pi_calc - math.pi):.6e}"}

    @staticmethod
    def hardy_ramanujan_partition_asymptotics(n: int) -> dict:
        """p(n) ~ (1 / (4 * n * sqrt(3))) * exp( pi * sqrt(2n / 3) )"""
        if n <= 0: raise ValueError("n must be positive.")
        exponent = math.pi * math.sqrt((2.0 * n) / 3.0)
        denom = 4.0 * n * math.sqrt(3.0)
        p_approx = (1.0 / denom) * math.exp(exponent)
        return {"n": n, "asymptotic_partition_p_n": round(p_approx, 2)}
