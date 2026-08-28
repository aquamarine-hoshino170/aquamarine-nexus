import math

class RelativisticHydroCore:
    C_LIGHT = 299792458.0

    @staticmethod
    def relativistic_sound_speed(adiabatic_index_gamma: float, pressure_pa: float, total_energy_density_j_m3: float) -> dict:
        """c_s = c * sqrt( gamma * P / (e + P) )"""
        if pressure_pa < 0 or total_energy_density_j_m3 <= 0:
            raise ValueError("Invalid enthalpy parameters.")
        
        h_enthalpy = total_energy_density_j_m3 + pressure_pa
        ratio = (adiabatic_index_gamma * pressure_pa) / h_enthalpy
        
        if ratio > 1.0:
            raise ValueError("Causality violated: sound speed exceeds light speed.")
        
        c_s = RelativisticHydroCore.C_LIGHT * math.sqrt(ratio)
        return {
            "sound_speed_m_s": f"{c_s:.6e}",
            "c_s_over_c": round(math.sqrt(ratio), 6)
        }

    @staticmethod
    def relativistic_bernoulli_invariant(lorentz_gamma: float, specific_enthalpy_h: float) -> dict:
        """B = gamma * h = constant along relativistic streamline"""
        if lorentz_gamma < 1.0 or specific_enthalpy_h <= 0:
            raise ValueError("Lorentz factor must be >= 1.")
        
        bernoulli_const = lorentz_gamma * specific_enthalpy_h
        return {"lorentz_gamma": lorentz_gamma, "bernoulli_invariant": round(bernoulli_const, 6)}
