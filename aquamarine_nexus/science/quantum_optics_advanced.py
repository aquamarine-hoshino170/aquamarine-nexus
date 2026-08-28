import math

class QuantumOpticsAdvancedCore:
    @staticmethod
    def coherent_state_photon_distribution(alpha_amplitude: float, photon_n: int) -> dict:
        """P(n) = exp(-|alpha|^2) * (|alpha|^(2n)) / n!"""
        if photon_n < 0:
            raise ValueError("Photon number n must be non-negative.")
        mean_photons = alpha_amplitude ** 2
        p_n = math.exp(-mean_photons) * (mean_photons ** photon_n) / math.factorial(photon_n)
        return {
            "coherent_alpha": alpha_amplitude,
            "mean_photon_number": round(mean_photons, 4),
            "n": photon_n,
            "probability_P_n": round(p_n, 8)
        }

    @staticmethod
    def optical_squeezing_variance(squeezing_param_r: float, anti_squeeze: bool = False) -> dict:
        """Var(X1) = (hbar/2) * exp(-2r), Var(X2) = (hbar/2) * exp(+2r)"""
        factor = math.exp(2.0 * squeezing_param_r) if anti_squeeze else math.exp(-2.0 * squeezing_param_r)
        variance_ratio = factor
        db_squeezing = -10.0 * math.log10(factor)
        return {
            "squeezing_r": squeezing_param_r,
            "quadrature_variance_factor": round(variance_ratio, 6),
            "squeezing_dB": round(db_squeezing, 2)
        }
