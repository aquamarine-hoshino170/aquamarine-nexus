import math

class EulerianStirlingCore:
    @staticmethod
    def eulerian_number_a(n: int, m: int) -> dict:
        """A(n, m) = sum_{k=0}^{m+1} (-1)^k * binom(n+1, k) * (m + 1 - k)^n"""
        if n < 0 or m < 0:
            raise ValueError("Indices must be non-negative.")
        if m >= n:
            return {"n": n, "m": m, "eulerian_A": 0}
        total = 0
        for k in range(m + 2):
            term = ((-1) ** k) * math.comb(n + 1, k) * ((m + 1 - k) ** n)
            total += term
        return {"n": n, "m": m, "eulerian_A": total}

    @staticmethod
    def stirling_first_kind_unsigned(n: int, k: int) -> dict:
        """|c(n, k)| recurrence: c(n, k) = (n - 1)*c(n - 1, k) + c(n - 1, k - 1)"""
        if n < 0 or k < 0:
            raise ValueError("Parameters must be non-negative.")
        if n == k == 0:
            return {"n": 0, "k": 0, "unsigned_stirling_s1": 1}
        if n == 0 or k == 0 or k > n:
            return {"n": n, "k": k, "unsigned_stirling_s1": 0}
        
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for i in range(1, n + 1):
            for j in range(1, min(i, k) + 1):
                dp[i][j] = (i - 1) * dp[i - 1][j] + dp[i - 1][j - 1]
        
        return {"n": n, "k": k, "unsigned_stirling_s1": dp[n][k]}
