import math

class ProteinThermodynamicsPureCore:
    R_GAS = 8.314462618

    @staticmethod
    def protein_folding_free_energy(fraction_unfolded: float, temp_k: float) -> dict:
        """K_eq = f_u / (1 - f_u), Delta_G = - R * T * ln(K_eq)"""
        if not (0.0 < fraction_unfolded < 1.0) or temp_k <= 0:
            raise ValueError("Fraction unfolded must be strictly in (0, 1) and temperature positive.")
        
        k_eq = fraction_unfolded / (1.0 - fraction_unfolded)
        delta_g = - ProteinThermodynamicsPureCore.R_GAS * temp_k * math.log(k_eq)
        
        return {
            "fraction_unfolded": round(fraction_unfolded, 4),
            "fraction_folded": round(1.0 - fraction_unfolded, 4),
            "equilibrium_constant_Keq": round(k_eq, 6),
            "delta_G_unfolding_J_mol": round(delta_g, 2),
            "folding_stability": "Native Folded Dominant" if delta_g > 0 else "Denatured/Unfolded Dominant"
        }

    @staticmethod
    def thermal_denaturation_melting_curve(temp_k: float, t_melting_k: float, delta_h_melting_j_mol: float) -> dict:
        """Delta_G(T) approx Delta_H_m * (1 - T / T_m)"""
        if t_melting_k <= 0 or temp_k <= 0 or delta_h_melting_j_mol <= 0:
            raise ValueError("Parameters must be strictly positive.")
            
        delta_g_t = delta_h_melting_j_mol * (1.0 - (temp_k / t_melting_k))
        k_eq = math.exp(-delta_g_t / (ProteinThermodynamicsPureCore.R_GAS * temp_k)) if (-delta_g_t / (ProteinThermodynamicsPureCore.R_GAS * temp_k)) < 700 else float('inf')
        f_u = k_eq / (1.0 + k_eq) if k_eq != float('inf') else 1.0
        
        return {
            "temperature_K": temp_k,
            "melting_temperature_Tm_K": t_melting_k,
            "delta_G_T_J_mol": round(delta_g_t, 2),
            "predicted_fraction_unfolded": round(f_u, 4)
        }
