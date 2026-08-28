import math

class PureLinalgCore:
    """Pure Python Linear Algebra Engine (Det, Norms, Cholesky, 2x2 Solver)"""

    @staticmethod
    def vector_norm(vector: list, p_order: int = 2) -> dict:
        """Computes L-p vector norm: ||x||_p = (sum |x_i|^p)^(1/p)"""
        if not vector:
            raise ValueError("Vector cannot be empty.")
        if p_order <= 0:
            raise ValueError("p_order must be positive.")

        norm_val = sum(abs(x) ** p_order for x in vector) ** (1.0 / p_order)
        return {
            "p_order": p_order,
            "vector_dimension": len(vector),
            "norm_value": round(norm_val, 6)
        }

    @staticmethod
    def matrix_trace(matrix: list) -> dict:
        """Computes trace of a square matrix: Tr(A) = sum(A_ii)"""
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("Matrix must be square.")

        trace_val = sum(matrix[i][i] for i in range(n))
        return {
            "dimension": n,
            "trace": round(trace_val, 6)
        }

    @staticmethod
    def solve_linear_2x2(a11: float, a12: float, a21: float, a22: float, b1: float, b2: float) -> dict:
        """
        Solves 2x2 linear system Ax = b via Cramer's Rule:
        [a11 a12] [x] = [b1]
        [a21 a22] [y]   [b2]
        """
        det_a = (a11 * a22) - (a12 * a21)
        if abs(det_a) < 1e-12:
            raise ValueError("System matrix is singular or near-singular (det = 0).")

        x = ((b1 * a22) - (b2 * a12)) / det_a
        y = ((a11 * b2) - (a21 * b1)) / det_a

        return {
            "determinant": round(det_a, 6),
            "solution_x": round(x, 6),
            "solution_y": round(y, 6)
        }

    @staticmethod
    def cholesky_decomposition_2x2(a11: float, a12: float, a22: float) -> dict:
        """
        Computes Cholesky factor L for positive-definite symmetric 2x2 matrix:
        A = L * L^T where L = [[l11, 0], [l21, l22]]
        """
        if a11 <= 0:
            raise ValueError("Matrix is not positive definite (a11 <= 0).")

        l11 = math.sqrt(a11)
        l21 = a12 / l11
        l22_sq = a22 - (l21 ** 2)

        if l22_sq <= 0:
            raise ValueError("Matrix is not positive definite.")

        l22 = math.sqrt(l22_sq)

        return {
            "L_matrix": [
                [round(l11, 6), 0.0],
                [round(l21, 6), round(l22, 6)]
            ]
        }
