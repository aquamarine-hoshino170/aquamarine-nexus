import math

class FloryHugginsPolymersCore:
    R_GAS = 8.314462618

    @staticmethod
    def flory_huggins_mixing_free_energy(phi_solvent: float, degree_polymerization_n: int, chi_parameter: float, temp_k: float = 298.15) -> dict:
        """Delta_G_m / (R*T) = phi_s * ln(phi_s) + (phi_p / N) * ln(phi_p) + chi * phi_s * phi_p"""
        if not (0.0 < phi_solvent < 1.0) or degree_polymerization_n < 1 or temp_k <= 0:
            raise ValueError("Solvent volume fraction must be in (0, 1), N >= 1, T > 0.")
            
        phi_p = 1.0 - phi_solvent
        term_s = phi_solvent * math.log(phi_solvent)
        term_p = (phi_p / degree_polymerization_n) * math.log(phi_p)
        term_interact = chi_parameter * phi_solvent * phi_p
        
        delta_g_over_rt = term_s + term_p + term_interact
        delta_g_joules = delta_g_over_rt * FloryHugginsPolymersCore.R_GAS * temp_k
        
        # Critical chi parameter for phase separation
        chi_crit = 0.5 * (1.0 + (1.0 / math.sqrt(degree_polymerization_n))) ** 2
        
        return {
            "phi_solvent": phi_solvent,
            "phi_polymer": round(phi_p, 4),
            "degree_polymerization_N": degree_polymerization_n,
            "flory_chi_parameter": chi_parameter,
            "critical_chi_bound": round(chi_crit, 6),
            "delta_G_mixing_J_mol": round(delta_g_joules, 4),
            "miscibility_state": "Single Homogeneous Phase" if chi_parameter < chi_crit else "Phase Separation / Spinodal Risk"
        }
