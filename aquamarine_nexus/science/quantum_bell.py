import math

class QuantumBellCore:
    """Quantum Entanglement, Bell Bases & CHSH Non-Locality Core"""

    @staticmethod
    def bell_state_amplitudes(state_name: str) -> dict:
        """
        Returns basis state amplitudes for the 4 maximally entangled 2-qubit Bell states:
        - 'phi_plus'  : (|00> + |11>) / sqrt(2)
        - 'phi_minus' : (|00> - |11>) / sqrt(2)
        - 'psi_plus'  : (|01> + |10>) / sqrt(2)
        - 'psi_minus' : (|01> - |10>) / sqrt(2)
        """
        inv_sqrt2 = 1.0 / math.sqrt(2.0)
        states = {
            "phi_plus": {"|00>": round(inv_sqrt2, 5), "|01>": 0.0, "|10>": 0.0, "|11>": round(inv_sqrt2, 5)},
            "phi_minus": {"|00>": round(inv_sqrt2, 5), "|01>": 0.0, "|10>": 0.0, "|11>": round(-inv_sqrt2, 5)},
            "psi_plus": {"|00>": 0.0, "|01>": round(inv_sqrt2, 5), "|10>": round(inv_sqrt2, 5), "|11>": 0.0},
            "psi_minus": {"|00>": 0.0, "|01>": round(inv_sqrt2, 5), "|10>": round(-inv_sqrt2, 5), "|11>": 0.0},
        }
        key = state_name.lower()
        if key not in states:
            raise ValueError(f"Unknown Bell state. Supported: {list(states.keys())}")
        return {"bell_state": state_name, "state_vector": states[key], "concurrence": 1.0}

    @staticmethod
    def chsh_inequality_correlation(theta_a: float, theta_a_prime: float, theta_b: float, theta_b_prime: float) -> dict:
        """
        Computes CHSH parameter S = E(a,b) - E(a,b') + E(a',b) + E(a',b') for singlet state |psi_minus>.
        Quantum bound (Tsirelson's bound): |S| <= 2*sqrt(2) approx 2.8284
        Classical local realism bound: |S| <= 2
        """
        # E(alpha, beta) = -cos(alpha - beta)
        def corr(alpha, beta):
            return -math.cos(alpha - beta)

        e_ab = corr(theta_a, theta_b)
        e_ab_p = corr(theta_a, theta_b_prime)
        e_ap_b = corr(theta_a_prime, theta_b)
        e_ap_bp = corr(theta_a_prime, theta_b_prime)

        s_val = e_ab - e_ab_p + e_ap_b + e_ap_bp

        return {
            "CHSH_S_parameter": round(s_val, 5),
            "violates_classical_bound": abs(s_val) > 2.0,
            "tsirelson_ratio": round(abs(s_val) / (2.0 * math.sqrt(2.0)), 5)
        }
