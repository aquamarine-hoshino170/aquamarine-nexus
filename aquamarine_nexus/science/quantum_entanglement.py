import math

class QuantumEntanglementCore:
    """Quantum Information Theory: Von Neumann Entropy, Purity & Entanglement Concurrence"""

    @staticmethod
    def von_neumann_entropy_diagonal(eigenvalues: list) -> dict:
        """
        Computes Von Neumann Entropy S(rho) = -sum(lambda_i * log2(lambda_i))
        from density matrix spectrum (eigenvalues sum to 1).
        """
        if not eigenvalues or abs(sum(eigenvalues) - 1.0) > 1e-4:
            raise ValueError("Eigenvalues must sum to 1.0 for valid density matrix.")

        entropy = 0.0
        purity = 0.0
        for l in eigenvalues:
            if l < 0.0:
                raise ValueError("Eigenvalues must be non-negative (positive semi-definite).")
            if l > 0.0:
                entropy -= l * math.log2(l)
            purity += l ** 2

        return {
            "von_neumann_entropy_bits": round(entropy, 6),
            "state_purity": round(purity, 6),
            "is_maximally_mixed": abs(entropy - math.log2(len(eigenvalues))) < 1e-5
        }

    @staticmethod
    def werner_state_concurrence(fraction_p: float) -> dict:
        """
        Calculates Entanglement Concurrence C(p) for 2-qubit Werner State rho = p|Psi-><Psi-| + (1-p)/4 * I:
        C(p) = max(0, (3p - 1) / 2)
        """
        if fraction_p < 0.0 or fraction_p > 1.0:
            raise ValueError("Werner fraction p must be within [0, 1].")

        concurrence = max(0.0, (3.0 * fraction_p - 1.0) / 2.0)
        return {
            "werner_parameter_p": fraction_p,
            "concurrence": round(concurrence, 6),
            "is_entangled": concurrence > 0.0
        }
