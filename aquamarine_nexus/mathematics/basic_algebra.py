import math

class BasicAlgebra:
    """Foundational Number Theory & Linear Algebra Engine"""
    @staticmethod
    def extended_gcd(a: int, b: int):
        """Extended Euclidean Algorithm: returns (gcd, x, y) such that ax + by = gcd"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = BasicAlgebra.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    @staticmethod
    def matrix_det_2x2(matrix: list):
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    @staticmethod
    def matrix_mul(A: list, B: list):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        if cols_A != rows_B:
            raise ValueError("Matrix dimension mismatch for multiplication.")
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return result

    @staticmethod
    def prime_factorization(n: int) -> dict:
        factors = {}
        d = 2
        while d * d <= n:
            while (n % d) == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors
