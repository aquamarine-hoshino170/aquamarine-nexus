import math

class OpenQuantumSystemsCore:
    @staticmethod
    def pure_dephasing_decay(coherence_rho01: float, dephasing_rate_gamma: float, time_t: float) -> dict:
        """rho_01(t) = rho_01(0) * exp(-Gamma * t)"""
        if dephasing_rate_gamma < 0 or time_t < 0:
            raise ValueError("Rate and time must be non-negative.")
        decay_factor = math.exp(-dephasing_rate_gamma * time_t)
        rho_t = coherence_rho01 * decay_factor
        return {
            "initial_coherence": coherence_rho01,
            "time_t": time_t,
            "decay_factor": round(decay_factor, 6),
            "coherence_at_t": round(rho_t, 6)
        }

    @staticmethod
    def thermal_lindblad_rates(transition_omega: float, temp_k: float, coupling_gamma0: float) -> dict:
        """gamma_down = gamma_0 * (n_th + 1), gamma_up = gamma_0 * n_th where n_th = 1/(exp(hbar*w/kT) - 1)"""
        hbar = 1.054571817e-34
        kb = 1.380649e-23
        if temp_k <= 0 or transition_omega <= 0 or coupling_gamma0 <= 0:
            raise ValueError("Inputs must be strictly positive.")
        
        x = (hbar * transition_omega) / (kb * temp_k)
        n_th = 1.0 / (math.exp(x) - 1.0) if x < 700 else 0.0
        gamma_down = coupling_gamma0 * (n_th + 1.0)
        gamma_up = coupling_gamma0 * n_th
        return {
            "thermal_photon_number_nth": round(n_th, 6),
            "emission_rate_gamma_down": round(gamma_down, 6),
            "absorption_rate_gamma_up": round(gamma_up, 6)
        }
