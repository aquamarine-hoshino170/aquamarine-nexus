import math

class QuantumChaosRMTCore:
    @staticmethod
    def wigner_surmise_goe(s_spacing: float) -> dict:
        """P_GOE(s) = (pi / 2) * s * exp(- (pi / 4) * s^2) for Gaussian Orthogonal Ensemble (Time-Reversal Invariant)"""
        if s_spacing < 0:
            raise ValueError("Spacing s must be non-negative.")
        prob = (math.pi / 2.0) * s_spacing * math.exp(- (math.pi / 4.0) * (s_spacing ** 2))
        return {
            "ensemble": "GOE (Gaussian Orthogonal)",
            "spacing_s": s_spacing,
            "probability_density": round(prob, 6)
        }

    @staticmethod
    def wigner_surmise_gue(s_spacing: float) -> dict:
        """P_GUE(s) = (32 / pi^2) * s^2 * exp(- (4 / pi) * s^2) for Gaussian Unitary Ensemble (Broken Time-Reversal)"""
        if s_spacing < 0:
            raise ValueError("Spacing s must be non-negative.")
        coeff = 32.0 / (math.pi ** 2)
        prob = coeff * (s_spacing ** 2) * math.exp(- (4.0 / math.pi) * (s_spacing ** 2))
        return {
            "ensemble": "GUE (Gaussian Unitary)",
            "spacing_s": s_spacing,
            "probability_density": round(prob, 6)
        }
