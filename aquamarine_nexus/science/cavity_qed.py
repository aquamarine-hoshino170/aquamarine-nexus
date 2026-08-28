import math

class CavityQEDCore:
    """Cavity Quantum Electrodynamics (CQED) & Jaynes-Cummings Interactions"""

    @staticmethod
    def rabi_oscillation_frequency(coupling_strength_g_hz: float, detuning_delta_hz: float = 0.0, photon_number_n: int = 0) -> dict:
        """
        Computes generalized Jaynes-Cummings Rabi Frequency:
        Omega_n = sqrt( Delta^2 + 4 * g^2 * (n + 1) )
        """
        if coupling_strength_g_hz < 0 or photon_number_n < 0:
            raise ValueError("Coupling strength and photon number must be non-negative.")

        g_eff_sq = 4.0 * (coupling_strength_g_hz ** 2) * (photon_number_n + 1)
        omega_n = math.sqrt((detuning_delta_hz ** 2) + g_eff_sq)

        return {
            "photon_number_n": photon_number_n,
            "vacuum_coupling_g_Hz": coupling_strength_g_hz,
            "detuning_Delta_Hz": detuning_delta_hz,
            "generalized_rabi_freq_Hz": round(omega_n, 4),
            "vacuum_rabi_splitting_Hz": round(2.0 * coupling_strength_g_hz, 4)
        }

    @staticmethod
    def excited_state_inversion(time_seconds: float, coupling_g_hz: float, photon_number_n: int = 0) -> dict:
        """
        Calculates atomic inversion W(t) = -cos(Omega_n * t) for resonant excitation (Delta = 0) starting in |e, n>
        """
        omega_n = 2.0 * coupling_g_hz * math.sqrt(photon_number_n + 1)
        inversion = math.cos(2.0 * math.pi * omega_n * time_seconds)

        return {
            "time_seconds": time_seconds,
            "population_inversion": round(inversion, 6),
            "excited_state_probability": round((1.0 + inversion) / 2.0, 6)
        }
