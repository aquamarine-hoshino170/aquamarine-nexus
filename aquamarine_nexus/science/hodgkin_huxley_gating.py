import math

class HodgkinHuxleyGatingCore:
    @staticmethod
    def sodium_activation_m_rates(v_membrane_mv: float) -> dict:
        """alpha_m = 0.1*(v + 40)/(1 - exp(-(v + 40)/10)), beta_m = 4.0*exp(-(v + 65)/18)"""
        v_rel = v_membrane_mv + 40.0
        if abs(v_rel) < 1e-7:
            alpha_m = 1.0  # L'Hopital limit
        else:
            alpha_m = (0.1 * v_rel) / (1.0 - math.exp(-v_rel / 10.0))
            
        beta_m = 4.0 * math.exp(-(v_membrane_mv + 65.0) / 18.0)
        m_inf = alpha_m / (alpha_m + beta_m)
        tau_m = 1.0 / (alpha_m + beta_m)
        
        return {
            "v_membrane_mV": v_membrane_mv,
            "alpha_m": round(alpha_m, 6),
            "beta_m": round(beta_m, 6),
            "m_steady_state_inf": round(m_inf, 6),
            "tau_m_ms": round(tau_m, 6)
        }

    @staticmethod
    def potassium_activation_n_rates(v_membrane_mv: float) -> dict:
        """alpha_n = 0.01*(v + 55)/(1 - exp(-(v + 55)/10)), beta_n = 0.125*exp(-(v + 65)/80)"""
        v_rel = v_membrane_mv + 55.0
        if abs(v_rel) < 1e-7:
            alpha_n = 0.1  # L'Hopital limit
        else:
            alpha_n = (0.01 * v_rel) / (1.0 - math.exp(-v_rel / 10.0))
            
        beta_n = 0.125 * math.exp(-(v_membrane_mv + 65.0) / 80.0)
        n_inf = alpha_n / (alpha_n + beta_n)
        tau_n = 1.0 / (alpha_n + beta_n)
        
        return {
            "v_membrane_mV": v_membrane_mv,
            "alpha_n": round(alpha_n, 6),
            "beta_n": round(beta_n, 6),
            "n_steady_state_inf": round(n_inf, 6),
            "tau_n_ms": round(tau_n, 6)
        }
