import math

class OpticalSolitonsNLSECore:
    @staticmethod
    def self_phase_modulation_shift(peak_power_watts: float, nonlinear_index_n2: float, effective_area_m2: float, length_m: float, wavelength_m: float) -> dict:
        """Phi_SPM = (2 * pi * n2 * P * L) / (lambda * A_eff)"""
        if effective_area_m2 <= 0 or wavelength_m <= 0 or length_m <= 0:
            raise ValueError("Physical dimensions and wavelength must be positive.")
        gamma_nl = (2.0 * math.pi * nonlinear_index_n2) / (wavelength_m * effective_area_m2)
        phi_max = gamma_nl * peak_power_watts * length_m
        return {
            "nonlinear_parameter_gamma_inv_W_m": f"{gamma_nl:.6e}",
            "max_spm_phase_shift_rad": round(phi_max, 4)
        }

    @staticmethod
    def fundamental_soliton_peak_power(beta2_dispersion_s2_m: float, pulse_duration_t0_s: float, gamma_nl: float) -> dict:
        """P_0 = |beta_2| / (gamma * T_0^2)"""
        if pulse_duration_t0_s <= 0 or gamma_nl <= 0 or beta2_dispersion_s2_m == 0:
            raise ValueError("Invalid pulse or fiber parameters.")
        p0 = abs(beta2_dispersion_s2_m) / (gamma_nl * (pulse_duration_t0_s ** 2))
        return {
            "pulse_duration_T0_s": f"{pulse_duration_t0_s:.6e}",
            "fundamental_soliton_power_W": round(p0, 4)
        }
