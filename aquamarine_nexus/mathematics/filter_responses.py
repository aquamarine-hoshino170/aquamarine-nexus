import math

class FilterResponsesCore:
    @staticmethod
    def butterworth_analog_magnitude(omega_rad_s: float, cutoff_omega_c: float, order_n: int) -> dict:
        """|H(j*omega)|^2 = 1 / ( 1 + (omega / omega_c)^(2*N) )"""
        if cutoff_omega_c <= 0 or order_n <= 0 or omega_rad_s < 0:
            raise ValueError("Invalid filter parameters.")
        ratio = omega_rad_s / cutoff_omega_c
        power_ratio = ratio ** (2 * order_n)
        mag_sq = 1.0 / (1.0 + power_ratio)
        mag_db = 10.0 * math.log10(mag_sq) if mag_sq > 0 else -100.0
        return {
            "frequency_ratio": round(ratio, 4),
            "magnitude_squared": round(mag_sq, 8),
            "attenuation_dB": round(mag_db, 4)
        }

    @staticmethod
    def quality_factor_damping(resonant_freq_hz: float, bandwidth_hz: float) -> dict:
        """Q = f_0 / Delta_f, zeta = 1 / (2 * Q)"""
        if resonant_freq_hz <= 0 or bandwidth_hz <= 0:
            raise ValueError("Frequencies must be positive.")
        q = resonant_freq_hz / bandwidth_hz
        zeta = 1.0 / (2.0 * q)
        return {
            "quality_factor_Q": round(q, 4),
            "damping_ratio_zeta": round(zeta, 6),
            "damping_regime": "Underdamped" if zeta < 1.0 else ("Critically Damped" if zeta == 1.0 else "Overdamped")
        }
