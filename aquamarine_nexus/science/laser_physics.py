import math

class LaserPhysicsCore:
    H_PLANCK = 6.62607015e-34
    C_LIGHT = 299792458.0

    @staticmethod
    def einstein_coefficients_relation(transition_freq_hz: float, a_spontaneous_rate_s: float) -> dict:
        """B_21 = (c^3 / (8 * pi * h * nu^3)) * A_21"""
        if transition_freq_hz <= 0 or a_spontaneous_rate_s <= 0:
            raise ValueError("Frequency and spontaneous rate must be positive.")
        nu = transition_freq_hz
        b_stimulated = (LaserPhysicsCore.C_LIGHT ** 3) / (8.0 * math.pi * LaserPhysicsCore.H_PLANCK * (nu ** 3)) * a_spontaneous_rate_s
        return {
            "frequency_Hz": f"{nu:.6e}",
            "einstein_A_s_inv": f"{a_spontaneous_rate_s:.6e}",
            "einstein_B_m3_J_s2": f"{b_stimulated:.6e}"
        }

    @staticmethod
    def laser_threshold_gain(cavity_length_m: float, mirror_r1: float, mirror_r2: float, internal_loss_alpha_m: float = 0.0) -> dict:
        """g_th = alpha_i + (1 / (2 * L)) * ln( 1 / (R1 * R2) )"""
        if cavity_length_m <= 0 or mirror_r1 <= 0 or mirror_r2 <= 0 or mirror_r1 > 1 or mirror_r2 > 1:
            raise ValueError("Invalid cavity mirrors or cavity length.")
        mirror_loss = (1.0 / (2.0 * cavity_length_m)) * math.log(1.0 / (mirror_r1 * mirror_r2))
        g_th = internal_loss_alpha_m + mirror_loss
        return {
            "cavity_length_m": cavity_length_m,
            "mirror_loss_per_m": round(mirror_loss, 6),
            "threshold_gain_g_th_per_m": round(g_th, 6)
        }
