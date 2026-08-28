import math

class QuantumHarmonicCore:
    H_BAR = 1.054571817e-34

    @staticmethod
    def harmonic_energy_eigenstate(level_n: int, angular_freq_omega: float) -> dict:
        """E_n = hbar * omega * (n + 1/2)"""
        if level_n < 0 or angular_freq_omega <= 0: raise ValueError("Invalid parameters.")
        e_joules = QuantumHarmonicCore.H_BAR * angular_freq_omega * (level_n + 0.5)
        return {"level_n": level_n, "energy_Joules": f"{e_joules:.6e}", "zero_point_energy_Joules": f"{0.5 * QuantumHarmonicCore.H_BAR * angular_freq_omega:.6e}"}

    @staticmethod
    def position_momentum_uncertainty(delta_x_m: float) -> dict:
        """sigma_p >= hbar / (2 * sigma_x)"""
        if delta_x_m <= 0: raise ValueError("delta_x must be positive.")
        min_delta_p = QuantumHarmonicCore.H_BAR / (2.0 * delta_x_m)
        return {"delta_x_m": delta_x_m, "min_delta_p_kg_m_s": f"{min_delta_p:.6e}"}
