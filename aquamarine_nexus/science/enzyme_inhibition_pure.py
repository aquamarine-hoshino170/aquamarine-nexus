class EnzymeInhibitionCore:
    @staticmethod
    def competitive_inhibition_rate(v_max: float, substrate_s: float, k_m: float, inhibitor_i: float, k_i: float) -> dict:
        """v = (V_max * [S]) / (K_m_app + [S]), where K_m_app = K_m * (1 + [I] / K_i)"""
        if v_max <= 0 or substrate_s < 0 or k_m <= 0 or inhibitor_i < 0 or k_i <= 0:
            raise ValueError("Parameters must be strictly positive.")
        
        alpha = 1.0 + (inhibitor_i / k_i)
        km_app = k_m * alpha
        v_rate = (v_max * substrate_s) / (km_app + substrate_s)
        
        return {
            "inhibition_type": "Competitive",
            "apparent_Km": round(km_app, 6),
            "v_max_effective": v_max,
            "reaction_velocity": round(v_rate, 6),
            "inhibition_factor_alpha": round(alpha, 4)
        }

    @staticmethod
    def uncompetitive_inhibition_rate(v_max: float, substrate_s: float, k_m: float, inhibitor_i: float, k_i_prime: float) -> dict:
        """v = ((V_max / alpha_prime) * [S]) / ((K_m / alpha_prime) + [S]), alpha_prime = 1 + [I]/K_i'"""
        if v_max <= 0 or substrate_s < 0 or k_m <= 0 or inhibitor_i < 0 or k_i_prime <= 0:
            raise ValueError("Parameters must be strictly positive.")
        
        alpha_prime = 1.0 + (inhibitor_i / k_i_prime)
        vmax_app = v_max / alpha_prime
        km_app = k_m / alpha_prime
        v_rate = (vmax_app * substrate_s) / (km_app + substrate_s)
        
        return {
            "inhibition_type": "Uncompetitive",
            "apparent_Vmax": round(vmax_app, 6),
            "apparent_Km": round(km_app, 6),
            "reaction_velocity": round(v_rate, 6)
        }
