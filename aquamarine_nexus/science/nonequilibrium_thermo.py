class NonEquilibriumThermoCore:
    """Linear Non-Equilibrium Thermodynamics & Onsager Reciprocal Relations"""

    @staticmethod
    def onsager_flux_and_entropy_production(l_matrix: list, thermodynamic_forces: list) -> dict:
        """
        Computes thermodynamic fluxes J_i = sum_j (L_ij * X_j) 
        and local entropy production rate sigma = sum_i (J_i * X_i) >= 0.
        l_matrix must be symmetric (Onsager reciprocity: L_ij = L_ji).
        """
        n = len(thermodynamic_forces)
        if len(l_matrix) != n or any(len(row) != n for row in l_matrix):
            raise ValueError("L-matrix dimension must match thermodynamic forces vector length.")

        for i in range(n):
            for j in range(i + 1, n):
                if abs(l_matrix[i][j] - l_matrix[j][i]) > 1e-6:
                    raise ValueError(f"Onsager reciprocity violated: L[{i}][{j}] != L[{j}][{i}]")

        fluxes = [0.0] * n
        for i in range(n):
            for j in range(n):
                fluxes[i] += l_matrix[i][j] * thermodynamic_forces[j]

        sigma = sum(j_val * x_val for j_val, x_val in zip(fluxes, thermodynamic_forces))

        return {
            "thermodynamic_fluxes_J": [round(f, 6) for f in fluxes],
            "entropy_production_rate_sigma": round(sigma, 6),
            "is_second_law_satisfied": sigma >= 0.0
        }
