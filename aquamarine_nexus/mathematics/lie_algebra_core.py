class LieAlgebraCore:
    @staticmethod
    def levi_civita_structure_constant(a: int, b: int, c: int) -> dict:
        """Levi-Civita epsilon_abc for SU(2) / SO(3) Lie Algebra structure constants [J_a, J_b] = i * epsilon_abc * J_c"""
        indices = (a, b, c)
        if set(indices) != {1, 2, 3}:
            epsilon = 0
        elif indices in [(1, 2, 3), (2, 3, 1), (3, 1, 2)]:
            epsilon = 1
        else:
            epsilon = -1
        return {"indices": [a, b, c], "epsilon_abc": epsilon}

    @staticmethod
    def su2_quadratic_casimir(spin_j: float) -> dict:
        """C_2(j) = j * (j + 1) * I"""
        if spin_j < 0 or (2 * spin_j) % 1 != 0:
            raise ValueError("Spin j must be non-negative half-integer or integer.")
        casimir_val = spin_j * (spin_j + 1.0)
        return {
            "spin_j": spin_j,
            "casimir_eigenvalue": round(casimir_val, 4),
            "representation_dimension": int(2 * spin_j + 1)
        }
