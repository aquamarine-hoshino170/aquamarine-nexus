import math

class NonlinearOpticsCore:
    """Nonlinear Photonics, Kerr Self-Focusing & Harmonic Generation"""

    @staticmethod
    def kerr_refractive_index(n0: float, n2_m2_w: float, intensity_w_m2: float) -> dict:
        """
        Optical Kerr Effect: n(I) = n0 + n2 * I
        Computes nonlinear refractive index and self-phase shift parameter.
        """
        if intensity_w_m2 < 0:
            raise ValueError("Intensity must be non-negative.")

        delta_n = n2_m2_w * intensity_w_m2
        n_total = n0 + delta_n

        return {
            "linear_index_n0": n0,
            "nonlinear_index_change": f"{delta_n:.6e}",
            "effective_index_n": round(n_total, 8)
        }

    @staticmethod
    def shg_conversion_efficiency(delta_k_rad_m: float, crystal_length_m: float, d_eff_pm_v: float = 2.0) -> dict:
        """
        Phase-matching sinc^2 function for Second Harmonic Generation (SHG):
        eta proportional to sinc^2(Delta_k * L / 2) = sin(u)^2 / u^2 where u = Delta_k * L / 2
        """
        if crystal_length_m <= 0:
            raise ValueError("Crystal length must be positive.")

        u = (delta_k_rad_m * crystal_length_m) / 2.0
        sinc_sq = (math.sin(u) / u) ** 2 if u != 0.0 else 1.0

        return {
            "phase_mismatch_delta_k": delta_k_rad_m,
            "crystal_length_m": crystal_length_m,
            "phase_matching_factor": round(sinc_sq, 6),
            "is_quasi_phase_matched": sinc_sq > 0.95
        }
