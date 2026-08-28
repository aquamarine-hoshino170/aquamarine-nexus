import math

class BornInfeldElectrodynamicsCore:
    EPSILON_0 = 8.8541878128e-12
    C_LIGHT = 299792458.0

    @staticmethod
    def born_infeld_energy_density(e_field_v_m: float, b_field_tesla: float, b_critical: float = 1.0e18) -> dict:
        """u_BI = b^2 * ( sqrt( 1 + (E^2 - c^2*B^2)/b^2 - (E.B)^2/(b^2*c^2) ) - 1 )"""
        if b_critical <= 0:
            raise ValueError("Critical field parameter must be strictly positive.")
        c = BornInfeldElectrodynamicsCore.C_LIGHT
        s = (e_field_v_m ** 2 - (c * b_field_tesla) ** 2) / (b_critical ** 2)
        if 1.0 + s < 0:
            raise ValueError("Field strength exceeds Born-Infeld non-linear singularity limit.")
        
        u_bi = (b_critical ** 2) * (math.sqrt(1.0 + s) - 1.0)
        u_maxwell = 0.5 * BornInfeldElectrodynamicsCore.EPSILON_0 * (e_field_v_m ** 2 + (c * b_field_tesla) ** 2)
        
        return {
            "e_field_V_m": f"{e_field_v_m:.6e}",
            "b_field_Tesla": f"{b_field_tesla:.6e}",
            "born_infeld_energy_density_J_m3": f"{u_bi:.6e}",
            "maxwell_linear_energy_density_J_m3": f"{u_maxwell:.6e}"
        }

    @staticmethod
    def vacuum_polarization_euler_heisenberg_shift(e_field_v_m: float) -> dict:
        """Delta_n = (2 * alpha^2 * hbar^3 / (45 * m_e^4 * c^5)) * E^2"""
        # Critical Schwinger Field E_S = 1.32e18 V/m
        e_schwinger = 1.32e18
        alpha = 1.0 / 137.035999
        ratio = e_field_v_m / e_schwinger
        delta_n = (2.0 * (alpha ** 2) / 45.0) * (ratio ** 2)
        return {
            "electric_field_V_m": f"{e_field_v_m:.6e}",
            "schwinger_field_ratio": f"{ratio:.6e}",
            "vacuum_refractive_index_shift": f"{delta_n:.6e}"
        }
