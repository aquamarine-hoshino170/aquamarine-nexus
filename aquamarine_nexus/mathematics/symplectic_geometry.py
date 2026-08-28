class SymplecticGeometryCore:
    """Pure Mathematics: Symplectic Manifolds, Poisson Brackets & Phase Flow"""

    @staticmethod
    def discrete_poisson_bracket_2d(df_dq: float, df_dp: float, dg_dq: float, dg_dp: float) -> dict:
        """
        Computes the canonical Poisson bracket {f, g} on 2D phase space:
        {f, g} = (df/dq * dg/dp) - (df/dp * dg/dq)
        """
        bracket = (df_dq * dg_dp) - (df_dp * dg_dq)

        return {
            "poisson_bracket_result": round(bracket, 8),
            "is_first_integral": abs(bracket) < 1e-12
        }

    @staticmethod
    def symplectic_matrix_invariance_2x2(matrix_2x2: list) -> dict:
        """
        Verifies whether a 2x2 matrix M belongs to the Symplectic Group Sp(2, R):
        Condition: M^T * J * M = J, where det(M) = 1
        """
        if len(matrix_2x2) != 2 or any(len(row) != 2 for row in matrix_2x2):
            raise ValueError("Matrix must be 2x2.")

        a, b = matrix_2x2[0][0], matrix_2x2[0][1]
        c, d = matrix_2x2[1][0], matrix_2x2[1][1]

        det_m = (a * d) - (b * c)
        is_symplectic = abs(det_m - 1.0) < 1e-7

        return {
            "matrix": matrix_2x2,
            "determinant": round(det_m, 8),
            "is_symplectic_Sp2R": is_symplectic
        }
