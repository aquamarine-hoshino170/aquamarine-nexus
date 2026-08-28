import math

class PhaseTransitionsChemistryCore:
    R_GAS = 8.314462618

    @staticmethod
    def clausius_clapeyron_vapor_pressure(p1_pa: float, t1_k: float, t2_k: float, delta_h_vap_j_mol: float) -> dict:
        """ln(P2 / P1) = - (Delta_H_vap / R) * (1/T2 - 1/T1)"""
        if p1_pa <= 0 or t1_k <= 0 or t2_k <= 0 or delta_h_vap_j_mol <= 0:
            raise ValueError("Pressures, temperatures, and enthalpy of vaporization must be positive.")
            
        r = PhaseTransitionsChemistryCore.R_GAS
        exponent = - (delta_h_vap_j_mol / r) * ((1.0 / t2_k) - (1.0 / t1_k))
        p2_pa = p1_pa * math.exp(exponent)
        
        return {
            "initial_pressure_P1_Pa": p1_pa,
            "initial_temp_T1_K": t1_k,
            "final_temp_T2_K": t2_k,
            "delta_H_vap_J_mol": delta_h_vap_j_mol,
            "vapor_pressure_P2_Pa": round(p2_pa, 4),
            "vapor_pressure_P2_atm": round(p2_pa / 101325.0, 6)
        }

    @staticmethod
    def trouton_rule_entropy_check(delta_h_vap_j_mol: float, boiling_temp_k: float) -> dict:
        """Delta_S_vap = Delta_H_vap / T_b approx 85 to 88 J/(mol*K)"""
        if boiling_temp_k <= 0 or delta_h_vap_j_mol <= 0:
            raise ValueError("Parameters must be positive.")
            
        delta_s = delta_h_vap_j_mol / boiling_temp_k
        is_trouton = (80.0 <= delta_s <= 95.0)
        
        return {
            "boiling_temp_Tb_K": boiling_temp_k,
            "vaporization_entropy_J_mol_K": round(delta_s, 3),
            "follows_trouton_rule": is_trouton,
            "deviation_nature": "Typical Non-associated Liquid" if is_trouton else ("Strong Hydrogen Bonding / Association" if delta_s > 95.0 else "Ordered Gas Phase")
        }
