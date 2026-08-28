class HeisenbergMechanicsCore:
    H_BAR = 1.054571817e-34

    @staticmethod
    def uncertainty_principle_limit(delta_x_m: float = None, delta_p_kg_m_s: float = None) -> dict:
        """Delta_x * Delta_p >= hbar / 2"""
        min_product = HeisenbergMechanicsCore.H_BAR / 2.0
        if delta_x_m is not None and delta_p_kg_m_s is None:
            if delta_x_m <= 0: raise ValueError("Position uncertainty must be positive.")
            min_dp = min_product / delta_x_m
            return {"delta_x_m": delta_x_m, "min_delta_p_kg_m_s": f"{min_dp:.6e}", "heisenberg_lower_bound": f"{min_product:.6e}"}
        elif delta_p_kg_m_s is not None and delta_x_m is None:
            if delta_p_kg_m_s <= 0: raise ValueError("Momentum uncertainty must be positive.")
            min_dx = min_product / delta_p_kg_m_s
            return {"delta_p_kg_m_s": delta_p_kg_m_s, "min_delta_x_m": f"{min_dx:.6e}", "heisenberg_lower_bound": f"{min_product:.6e}"}
        elif delta_x_m is not None and delta_p_kg_m_s is not None:
            prod = delta_x_m * delta_p_kg_m_s
            return {"uncertainty_product": f"{prod:.6e}", "heisenberg_lower_bound": f"{min_product:.6e}", "satisfies_uncertainty": prod >= min_product}
        else:
            raise ValueError("Provide delta_x, delta_p, or both.")

    @staticmethod
    def commutator_bracket_2x2(matrix_a: list, matrix_b: list) -> dict:
        """[A, B] = A*B - B*A"""
        if len(matrix_a) != 2 or len(matrix_b) != 2 or any(len(r) != 2 for r in matrix_a + matrix_b):
            raise ValueError("Must be 2x2 matrices.")
        
        def matmul(m1, m2):
            return [
                [m1[0][0]*m2[0][0] + m1[0][1]*m2[1][0], m1[0][0]*m2[0][1] + m1[0][1]*m2[1][1]],
                [m1[1][0]*m2[0][0] + m1[1][1]*m2[1][0], m1[1][0]*m2[0][1] + m1[1][1]*m2[1][1]]
            ]
        
        ab = matmul(matrix_a, matrix_b)
        ba = matmul(matrix_b, matrix_a)
        comm = [[ab[i][j] - ba[i][j] for j in range(2)] for i in range(2)]
        is_commuting = all(abs(comm[i][j]) < 1e-12 for i in range(2) for j in range(2))
        return {"commutator_matrix": comm, "is_commuting": is_commuting}
