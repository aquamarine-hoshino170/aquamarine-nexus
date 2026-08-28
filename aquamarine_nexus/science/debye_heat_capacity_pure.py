import math

class DebyeHeatCapacityCore:
    R_GAS = 8.314462618

    @staticmethod
    def debye_low_temperature_limit(temp_k: float, debye_temp_k: float, moles_n: float = 1.0) -> dict:
        """C_v = (12 * pi^4 / 5) * n * R * (T / Theta_D)^3 for T << Theta_D"""
        if temp_k <= 0 or debye_temp_k <= 0 or moles_n <= 0:
            raise ValueError("Temperature, Debye temperature, and moles must be strictly positive.")
            
        ratio = temp_k / debye_temp_k
        if ratio > 0.15:
            regime = "High-Temperature Deviation (Requires Full Numerical Integral)"
        else:
            regime = "T^3 Phonon Low-Temperature Regime"
            
        c_v_coeff = (12.0 * (math.pi ** 4) / 5.0) * moles_n * DebyeHeatCapacityCore.R_GAS
        c_v = c_v_coeff * (ratio ** 3)
        
        return {
            "temperature_K": temp_k,
            "debye_temperature_ThetaD_K": debye_temp_k,
            "temperature_ratio_T_over_TD": round(ratio, 6),
            "molar_heat_capacity_Cv_J_mol_K": round(c_v, 6),
            "regime": regime
        }
