import math

class MaxwellElectrodynamicsCore:
    EPSILON_0 = 8.8541878128e-12
    MU_0 = 1.25663706212e-6

    @staticmethod
    def speed_of_light_from_constants() -> dict:
        """c = 1 / sqrt(mu_0 * epsilon_0)"""
        c_calc = 1.0 / math.sqrt(MaxwellElectrodynamicsCore.MU_0 * MaxwellElectrodynamicsCore.EPSILON_0)
        return {"epsilon_0": MaxwellElectrodynamicsCore.EPSILON_0, "mu_0": MaxwellElectrodynamicsCore.MU_0, "calculated_speed_of_light_m_s": round(c_calc, 2)}

    @staticmethod
    def poynting_vector_magnitude(electric_field_v_m: float, magnetic_field_tesla: float) -> dict:
        """S = (E * B) / mu_0"""
        s_val = (electric_field_v_m * magnetic_field_tesla) / MaxwellElectrodynamicsCore.MU_0
        return {"E_field_V_m": electric_field_v_m, "B_field_Tesla": magnetic_field_tesla, "poynting_vector_W_m2": f"{s_val:.6e}"}
