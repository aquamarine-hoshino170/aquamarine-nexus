from typing import List

class StrassenWinogradGEMM:
    """
    Zero-Dependency Sub-Cubic Matrix Multiplication Core.
    Reduces standard O(N^3) arithmetic complexity down to O(N^2.807) using
    Winograd's variant of Strassen's 7-multiplication decomposition.
    """

    @staticmethod
    def _pad_matrix(A: List[List[float]], target_dim: int) -> List[List[float]]:
        n = len(A)
        padded = [[0.0] * target_dim for _ in range(target_dim)]
        for i in range(n):
            for j in range(len(A[0])):
                padded[i][j] = A[i][j]
        return padded

    @staticmethod
    def _next_power_of_two(n: int) -> int:
        return 1 << (n - 1).bit_length()

    @staticmethod
    def _add(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        n = len(A)
        return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

    @staticmethod
    def _sub(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        n = len(A)
        return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

    @classmethod
    def _strassen_recursive(cls, A: List[List[float]], B: List[List[float]], leaf_size: int = 32) -> List[List[float]]:
        n = len(A)
        if n <= leaf_size:
            # Base case: Standard blocked loop
            C = [[0.0] * n for _ in range(n)]
            for i in range(n):
                for k in range(n):
                    a_ik = A[i][k]
                    for j in range(n):
                        C[i][j] += a_ik * B[k][j]
            return C

        mid = n // 2

        # 4 Sub-matrices partitioning
        A11 = [row[:mid] for row in A[:mid]]
        A12 = [row[mid:] for row in A[:mid]]
        A21 = [row[:mid] for row in A[mid:]]
        A22 = [row[mid:] for row in A[mid:]]

        B11 = [row[:mid] for row in B[:mid]]
        B12 = [row[mid:] for row in B[mid:]]
        B21 = [row[:mid] for row in B[mid:]]
        B22 = [row[mid:] for row in B[mid:]]

        # Strassen 7 recursive products
        M1 = cls._strassen_recursive(cls._add(A11, A22), cls._add(B11, B22), leaf_size)
        M2 = cls._strassen_recursive(cls._add(A21, A22), B11, leaf_size)
        M3 = cls._strassen_recursive(A11, cls._sub(B12, B22), leaf_size)
        M4 = cls._strassen_recursive(A22, cls._sub(B21, B11), leaf_size)
        M5 = cls._strassen_recursive(cls._add(A11, A12), B22, leaf_size)
        M6 = cls._strassen_recursive(cls._sub(A21, A11), cls._add(B11, B12), leaf_size)
        M7 = cls._strassen_recursive(cls._sub(A12, A22), cls._add(B21, B22), leaf_size)

        # Output blocks construction
        C11 = cls._add(cls._sub(cls._add(M1, M4), M5), M7)
        C12 = cls._add(M3, M5)
        C21 = cls._add(M2, M4)
        C22 = cls._add(cls._add(cls._sub(M1, M2), M3), M6)

        # Merge blocks
        C = [[0.0] * n for _ in range(n)]
        for i in range(mid):
            for j in range(mid):
                C[i][j] = C11[i][j]
                C[i][j + mid] = C12[i][j]
                C[i + mid][j] = C21[i][j]
                C[i + mid][j + mid] = C22[i][j]

        return C

    @classmethod
    def multiply(cls, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        r_a, c_a = len(A), len(A[0])
        r_b, c_b = len(B), len(B[0])
        if c_a != r_b:
            raise ValueError(f"Matrix shape mismatch: ({r_a}x{c_a}) and ({r_b}x{c_b})")

        max_dim = max(r_a, c_a, c_b)
        pow2_dim = cls._next_power_of_two(max_dim)

        padded_A = cls._pad_matrix(A, pow2_dim)
        padded_B = cls._pad_matrix(B, pow2_dim)

        padded_C = cls._strassen_recursive(padded_A, padded_B, leaf_size=32)

        # Unpad
        return [padded_C[i][:c_b] for i in range(r_a)]
