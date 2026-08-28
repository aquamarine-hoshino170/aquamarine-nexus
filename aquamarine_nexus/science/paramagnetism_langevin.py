import math

class LangevinParamagnetismCore:
    K_BOLTZ = 1.380649e-23
    MU_0 = 1.25663706212e-6

    @staticmethod
    def langevin_magnetization(magnetic_moment_j_t: float, b_field_tesla: float, temp_k: float, spin_density_m3: float) -> dict:
        """M = M_s * L(xi) where L(xi) = coth(xi) - 1/xi and xi = (mu * B) / (k_B * T)"""
        if magnetic_moment_j_t <= 0 or b_field_tesla < 0 or temp_k <= 0 or spin_density_m3 <= 0:
            raise ValueError("Invalid parameters.")
            
        xi = (magnetic_moment_j_t * b_field_tesla) / (LangevinParamagnetismCore.K_BOLTZ * temp_k)
        
        if xi < 1e-4:
            # Taylor expansion for small xi (Curie's Law regime: L(xi) approx xi / 3)
            l_xi = xi / 3.0
        elif xi > 700:
            l_xi = 1.0
        else:
            coth_xi = (math.exp(xi) + math.exp(-xi)) / (math.exp(xi) - math.exp(-xi))
            l_xi = coth_xi - (1.0 / xi)
            
        m_saturation = spin_density_m3 * magnetic_moment_j_t
        m_actual = m_saturation * l_xi
        
        return {
            "xi_langevin_parameter": round(xi, 6),
            "langevin_function_L_xi": round(l_xi, 6),
            "saturation_magnetization_A_m": f"{m_saturation:.6e}",
            "magnetization_M_A_m": f"{m_actual:.6e}"
        }
