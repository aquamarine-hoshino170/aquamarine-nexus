import math

class FluidMechanicsCore:
    @staticmethod
    def reynolds_number(density_kg_m3: float, velocity_m_s: float, char_length_m: float, dynamic_viscosity_pa_s: float) -> dict:
        """Re = (rho * v * L) / mu"""
        if dynamic_viscosity_pa_s <= 0 or char_length_m <= 0 or density_kg_m3 <= 0: raise ValueError("Invalid inputs.")
        re = (density_kg_m3 * velocity_m_s * char_length_m) / dynamic_viscosity_pa_s
        regime = "Laminar" if re < 2300 else ("Transitional" if re <= 4000 else "Turbulent")
        return {"reynolds_number": round(re, 2), "flow_regime": regime}

    @staticmethod
    def poiseuille_volumetric_flow(radius_m: float, delta_p_pa: float, length_m: float, dynamic_viscosity_pa_s: float) -> dict:
        """Q = (pi * R^4 * Delta_P) / (8 * mu * L)"""
        if radius_m <= 0 or length_m <= 0 or dynamic_viscosity_pa_s <= 0: raise ValueError("Invalid inputs.")
        q = (math.pi * (radius_m ** 4) * delta_p_pa) / (8.0 * dynamic_viscosity_pa_s * length_m)
        return {"volumetric_flow_m3_s": f"{q:.6e}", "flow_liters_per_min": round(q * 60000.0, 4)}

    @staticmethod
    def mach_number_and_stagnation_temp(velocity_m_s: float, ambient_temp_k: float, gamma_ratio: float = 1.4, gas_constant_r: float = 287.05) -> dict:
        """M = v / sqrt(gamma * R * T), T_0 = T * (1 + (gamma-1)/2 * M^2)"""
        if ambient_temp_k <= 0: raise ValueError("Temperature must be positive.")
        c_sound = math.sqrt(gamma_ratio * gas_constant_r * ambient_temp_k)
        mach = velocity_m_s / c_sound
        t_0 = ambient_temp_k * (1.0 + 0.5 * (gamma_ratio - 1.0) * (mach ** 2))
        return {"speed_of_sound_m_s": round(c_sound, 2), "mach_number": round(mach, 4), "stagnation_temperature_K": round(t_0, 2)}
