import math

class MegaChemistryCore:
    R_GAS = 8.314462618
    H_PLANCK = 6.62607015e-34
    K_BOLTZ = 1.380649e-23

    @staticmethod
    def eyring_transition_state_rate(delta_h_activation_j_mol: float, delta_s_activation_j_mol_k: float, temp_k: float) -> dict:
        """k = (k_B * T / h) * exp(Delta_S# / R) * exp(-Delta_H# / (R*T))"""
        if temp_k <= 0: raise ValueError("Temperature must be strictly positive.")
        kb = MegaChemistryCore.K_BOLTZ
        h = MegaChemistryCore.H_PLANCK
        r = MegaChemistryCore.R_GAS
        
        prefactor = (kb * temp_k) / h
        entropy_term = math.exp(delta_s_activation_j_mol_k / r)
        enthalpy_term = math.exp(-delta_h_activation_j_mol / (r * temp_k))
        k_rate = prefactor * entropy_term * enthalpy_term
        
        return {
            "temperature_K": temp_k,
            "delta_H_activation_J_mol": delta_h_activation_j_mol,
            "delta_S_activation_J_mol_K": delta_s_activation_j_mol_k,
            "eyring_rate_constant_k": f"{k_rate:.6e}"
        }

    @staticmethod
    def crystal_field_stabilization_energy(d_electrons: int, high_spin: bool, delta_oct_cm1: float, pairing_energy_cm1: float = 15000.0) -> dict:
        """CFSE = ( -0.4 * n_t2g + 0.6 * n_eg ) * Delta_oct + P_correction"""
        if not (0 <= d_electrons <= 10) or delta_oct_cm1 <= 0:
            raise ValueError("d electrons must be in range 0-10.")
        
        if d_electrons <= 3:
            t2g, eg, pairs = d_electrons, 0, 0
        elif high_spin:
            if d_electrons <= 5: t2g, eg, pairs = 3, d_electrons - 3, 0
            elif d_electrons <= 8: t2g, eg, pairs = d_electrons - 2, 2, d_electrons - 5
            else: t2g, eg, pairs = 6, d_electrons - 6, d_electrons - 5
        else:  # Low spin
            if d_electrons <= 6: t2g, eg, pairs = d_electrons, 0, max(0, d_electrons - 3)
            else: t2g, eg, pairs = 6, d_electrons - 6, max(0, d_electrons - 5)
            
        cfse_delta = (-0.4 * t2g + 0.6 * eg)
        cfse_energy = cfse_delta * delta_oct_cm1
        
        return {
            "d_electron_count": d_electrons,
            "spin_state": "High Spin" if high_spin else "Low Spin",
            "t2g_occupancy": t2g,
            "eg_occupancy": eg,
            "cfse_octahedral_Delta_units": round(cfse_delta, 2),
            "cfse_energy_cm_minus1": round(cfse_energy, 2)
        }

    @staticmethod
    def beer_lambert_molar_absorptivity(absorbance_a: float, path_length_cm: float, concentration_molar: float) -> dict:
        """A = epsilon * c * l => epsilon = A / (c * l)"""
        if absorbance_a < 0 or path_length_cm <= 0 or concentration_molar <= 0:
            raise ValueError("Invalid parameters.")
        eps = absorbance_a / (concentration_molar * path_length_cm)
        transmittance = 10.0 ** (-absorbance_a)
        return {
            "absorbance": absorbance_a,
            "transmittance_T": round(transmittance, 6),
            "molar_extinction_coefficient_M_cm": round(eps, 4)
        }
