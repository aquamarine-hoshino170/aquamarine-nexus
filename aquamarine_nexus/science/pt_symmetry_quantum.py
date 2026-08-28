import math

class PTSymmetryQuantumCore:
    @staticmethod
    def pt_symmetric_2x2_spectrum(delta_detuning: float, non_hermitian_gain_gamma: float, coupling_g: float) -> dict:
        """H = [[delta - i*gamma, g], [g, -delta + i*gamma]] -> E = +- sqrt(delta^2 + g^2 - gamma^2 - 2*i*delta*gamma)"""
        # For symmetric branch (delta = 0): E = +- sqrt(g^2 - gamma^2)
        disc = (coupling_g ** 2) - (non_hermitian_gain_gamma ** 2)
        if disc > 0:
            e_val = math.sqrt(disc)
            regime = "Exact PT-Symmetric Phase (Real Eigenvalues)"
            e_str = f"+- {round(e_val, 6)}"
        elif disc < 0:
            e_val = math.sqrt(-disc)
            regime = "Broken PT-Symmetric Phase (Complex Conjugate Pairs)"
            e_str = f"+- {round(e_val, 6)} j"
        else:
            e_val = 0.0
            regime = "Exceptional Point (EP2 Coalescence)"
            e_str = "0.0 (Degenerate Defective)"

        return {
            "coupling_g": coupling_g,
            "gain_loss_gamma": non_hermitian_gain_gamma,
            "eigenvalues": e_str,
            "phase_regime": regime,
            "distance_to_exceptional_point": round(abs(coupling_g - non_hermitian_gain_gamma), 6)
        }

    @staticmethod
    def non_unitary_norm_dynamics(initial_norm: float, gamma_gain: float, time_t: float) -> dict:
        """P(t) proxy in non-Hermitian system"""
        factor = math.cosh(2.0 * gamma_gain * time_t)
        norm_t = initial_norm * factor
        return {
            "initial_norm": initial_norm,
            "time_t": time_t,
            "amplification_factor": round(factor, 6),
            "state_norm_at_t": round(norm_t, 6)
        }
