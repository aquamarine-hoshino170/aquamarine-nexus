import math

class ElectrochemistryPureCore:
    R_GAS = 8.314462618
    F_FARADAY = 96485.33212

    @staticmethod
    def nernst_cell_potential(standard_e0_v: float, reaction_quotient_q: float, electrons_n: int, temp_k: float = 298.15) -> dict:
        """E = E0 - (R*T / (n*F)) * ln(Q)"""
        if reaction_quotient_q <= 0 or electrons_n <= 0 or temp_k <= 0:
            raise ValueError("Invalid parameters.")
        
        rt_over_nf = (ElectrochemistryPureCore.R_GAS * temp_k) / (electrons_n * ElectrochemistryPureCore.F_FARADAY)
        delta_v = rt_over_nf * math.log(reaction_quotient_q)
        e_cell = standard_e0_v - delta_v
        delta_g = - electrons_n * ElectrochemistryPureCore.F_FARADAY * e_cell
        
        return {
            "standard_E0_V": standard_e0_v,
            "reaction_quotient_Q": reaction_quotient_q,
            "electrons_transferred_n": electrons_n,
            "cell_potential_E_V": round(e_cell, 6),
            "gibbs_free_energy_Delta_G_J": round(delta_g, 2),
            "is_spontaneous": delta_g < 0
        }

    @staticmethod
    def faraday_electrolysis_mass(current_amperes: float, time_seconds: float, molar_mass_g_mol: float, valence_z: int) -> dict:
        """m = (I * t * M) / (z * F)"""
        if current_amperes <= 0 or time_seconds <= 0 or molar_mass_g_mol <= 0 or valence_z <= 0:
            raise ValueError("All parameters must be positive.")
            
        charge_coulombs = current_amperes * time_seconds
        mass_grams = (charge_coulombs * molar_mass_g_mol) / (valence_z * ElectrochemistryPureCore.F_FARADAY)
        
        return {
            "charge_Coulombs": round(charge_coulombs, 4),
            "deposited_mass_grams": round(mass_grams, 6)
        }
