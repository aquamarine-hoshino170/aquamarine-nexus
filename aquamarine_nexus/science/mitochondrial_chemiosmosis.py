import math

class MitochondrialChemiosmosisCore:
    R_GAS = 8.314462618
    F_FARADAY = 96485.33212

    @staticmethod
    def proton_motive_force(delta_psi_mv: float, delta_ph: float, temp_k: float = 310.15) -> dict:
        """Delta_p = Delta_Psi - (2.302585 * R * T / F) * Delta_pH (in mV)"""
        if temp_k <= 0:
            raise ValueError("Temperature must be strictly positive.")
            
        rt_over_f_factor = (math.log(10.0) * MitochondrialChemiosmosisCore.R_GAS * temp_k) / MitochondrialChemiosmosisCore.F_FARADAY * 1000.0
        ph_contribution_mv = rt_over_f_factor * delta_ph
        delta_p_mv = delta_psi_mv - ph_contribution_mv
        
        # Delta G = - F * Delta_p (J/mol)
        delta_g_j_mol = - (MitochondrialChemiosmosisCore.F_FARADAY * (delta_p_mv / 1000.0))
        delta_g_kj_mol = delta_g_j_mol / 1000.0
        
        return {
            "membrane_potential_Delta_Psi_mV": delta_psi_mv,
            "ph_gradient_Delta_pH": delta_ph,
            "chemical_gradient_contribution_mV": round(ph_contribution_mv, 2),
            "total_proton_motive_force_Delta_p_mV": round(delta_p_mv, 2),
            "free_energy_per_mole_H_kJ_mol": round(delta_g_kj_mol, 3),
            "bioenergetic_state": "Sufficient for ATP Synthesis" if abs(delta_p_mv) >= 150.0 else "Sub-threshold PMF"
        }
