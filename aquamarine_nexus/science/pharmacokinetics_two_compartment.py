import math

class PharmacokineticsCore:
    @staticmethod
    def two_compartment_iv_bolus(dose_mg: float, v_central_l: float, k10_elim: float, k12_dist: float, k21_redist: float, time_hr: float) -> dict:
        """C(t) = A * exp(-alpha * t) + B * exp(-beta * t)"""
        if any(x <= 0 for x in [dose_mg, v_central_l, k10_elim, k12_dist, k21_redist]) or time_hr < 0:
            raise ValueError("Parameters and dose must be strictly positive.")
            
        sum_k = k10_elim + k12_dist + k21_redist
        prod_k = k10_elim * k21_redist
        disc = math.sqrt(max(0.0, (sum_k ** 2) - (4.0 * prod_k)))
        
        alpha = 0.5 * (sum_k + disc)
        beta = 0.5 * (sum_k - disc)
        
        c0 = dose_mg / v_central_l
        a_coeff = c0 * (alpha - k21_redist) / (alpha - beta)
        b_coeff = c0 * (k21_redist - beta) / (alpha - beta)
        
        c_t = (a_coeff * math.exp(-alpha * time_hr)) + (b_coeff * math.exp(-beta * time_hr))
        
        return {
            "time_hr": time_hr,
            "distribution_hybrid_alpha": round(alpha, 6),
            "elimination_hybrid_beta": round(beta, 6),
            "plasma_concentration_mg_L": round(c_t, 6),
            "distribution_half_life_hr": round(math.log(2.0) / alpha, 4),
            "elimination_half_life_hr": round(math.log(2.0) / beta, 4)
        }
