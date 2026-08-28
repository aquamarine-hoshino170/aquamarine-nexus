import math

class NexusNDArray:
    """Pure-Python N-D Array & Linear Algebra Tensor Core (NumPy Alternative)"""
    def __init__(self, data):
        if isinstance(data, (int, float)):
            self.data = [float(data)]
            self.shape = (1,)
        elif isinstance(data, list):
            self.data = data
            self.shape = self._get_shape(data)
        else:
            raise TypeError("Data must be a list or scalar numeric.")

    def _get_shape(self, lst):
        if not isinstance(lst, list):
            return ()
        return (len(lst),) + self._get_shape(lst[0]) if lst else (0,)

    @staticmethod
    def zeros(rows: int, cols: int):
        return [[0.0 for _ in range(cols)] for _ in range(rows)]

    @staticmethod
    def eye(n: int):
        mat = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            mat[i][i] = 1.0
        return mat

    @staticmethod
    def matmul(A: list, B: list) -> list:
        rA, cA = len(A), len(A[0])
        rB, cB = len(B), len(B[0])
        if cA != rB:
            raise ValueError(f"Shape mismatch: {cA} != {rB}")
        out = [[sum(A[i][k] * B[k][j] for k in range(cA)) for j in range(cB)] for i in range(rA)]
        return out

    @staticmethod
    def lu_decompose(A: list):
        """Doolittle Algorithm for LU Decomposition (A = L * U)"""
        n = len(A)
        L = NexusNDArray.eye(n)
        U = NexusNDArray.zeros(n, n)
        for i in range(n):
            for k in range(i, n):
                s = sum(L[i][j] * U[j][k] for j in range(i))
                U[i][k] = A[i][k] - s
            for k in range(i + 1, n):
                s = sum(L[k][j] * U[j][i] for j in range(i))
                if U[i][i] == 0:
                    raise ZeroDivisionError("Singular matrix encountered in LU.")
                L[k][i] = (A[k][i] - s) / U[i][i]
        return L, U

    @staticmethod
    def matrix_inverse(A: list) -> list:
        """Invert matrix using LU Back-substitution"""
        n = len(A)
        L, U = NexusNDArray.lu_decompose(A)
        inv = NexusNDArray.zeros(n, n)
        for c in range(n):
            # Forward solve Ly = e_c
            y = [0.0] * n
            for i in range(n):
                s = sum(L[i][j] * y[j] for j in range(i))
                y[i] = (1.0 if i == c else 0.0) - s
            # Backward solve Ux = y
            x = [0.0] * n
            for i in range(n - 1, -1, -1):
                s = sum(U[i][j] * x[j] for j in range(i + 1, n))
                x[i] = (y[i] - s) / U[i][i]
            for r in range(n):
                inv[r][c] = round(x[r], 6)
        return inv

    @staticmethod
    def power_iteration_eigen(A: list, num_iter: int = 50) -> dict:
        """Computes dominant eigenvalue and eigenvector"""
        n = len(A)
        b_k = [1.0] * n
        for _ in range(num_iter):
            # Multiply A * b_k
            b_k1 = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
            norm = math.sqrt(sum(x**2 for x in b_k1))
            b_k = [x / norm for x in b_k1]
        
        # Rayleigh quotient for eigenvalue
        Ab = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        eigenval = sum(b_k[i] * Ab[i] for i in range(n))
        return {"dominant_eigenvalue": round(eigenval, 6), "eigenvector": [round(x, 5) for x in b_k]}
