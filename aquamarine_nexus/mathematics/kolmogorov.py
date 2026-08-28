import math

class AlgorithmicComplexityCore:
    """Algorithmic Information Theory & Lempel-Ziv Complexity Proxy"""

    @staticmethod
    def lempel_ziv_complexity(binary_string: str) -> dict:
        """
        Computes Lempel-Ziv (LZ76) algorithmic complexity for binary/symbolic strings.
        Measures structural compressibility and algorithmic randomness.
        """
        s = str(binary_string)
        n = len(s)
        if n == 0:
            return {"length": 0, "complexity_c": 0, "normalized_complexity": 0.0}

        i = 0
        k = 1
        l = 1
        k_max = 1
        c = 1

        while True:
            if s[i + k - 1] == s[l + k - 1]:
                k += 1
                if l + k > n:
                    c += 1
                    break
            else:
                if k > k_max:
                    k_max = k
                i += 1
                if i == l:
                    c += 1
                    l += k_max
                    if l + 1 > n:
                        break
                    i = 0
                    k = 1
                    k_max = 1
                else:
                    k = 1

        # Normalized complexity b(n) = n / log2(n)
        b_n = n / math.log2(n) if n > 1 else 1.0
        normalized = c / b_n

        return {
            "sequence_length": n,
            "lz_complexity_c": c,
            "normalized_complexity": round(normalized, 5),
            "is_algorithmically_random": normalized > 0.9
        }
