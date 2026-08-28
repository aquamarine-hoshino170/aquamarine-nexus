class PartitionTheoryCore:
    @staticmethod
    def integer_partition_count(n: int) -> dict:
        """Exact integer partition function p(n) via Euler's Pentagonal Number recurrence"""
        if n < 0 or n > 100:
            raise ValueError("n must be within [0, 100].")
        p = [1] + [0] * n
        for i in range(1, n + 1):
            val = 0
            k = 1
            while True:
                # Generalized pentagonal numbers: gk = (3*k^2 - k)//2 and (3*k^2 + k)//2
                g1 = (3 * k * k - k) // 2
                g2 = (3 * k * k + k) // 2
                sign = 1 if (k % 2 == 1) else -1
                
                if g1 <= i:
                    val += sign * p[i - g1]
                if g2 <= i:
                    val += sign * p[i - g2]
                if g1 > i and g2 > i:
                    break
                k += 1
            p[i] = val
        return {"n": n, "partition_count_p_n": p[n]}

    @staticmethod
    def generalized_pentagonal_number(k_index: int) -> dict:
        """g_k = (3*k^2 - k) / 2 for k in Z"""
        g_k = (3 * (k_index ** 2) - k_index) // 2
        return {"k": k_index, "pentagonal_number": g_k}
