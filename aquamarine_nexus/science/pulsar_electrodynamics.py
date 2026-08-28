import math

class PulsarElectrodynamicsCore:
    C_LIGHT = 299792458.0
    M_NEUTRON_STAR = 1.4 * 1.989e30
    R_NEUTRON_STAR = 10000.0  # 10 km

    @staticmethod
    def pulsar_spindown_luminosity(period_seconds: float, p_dot: float) -> dict:
        """E_dot = 4 * pi^2 * I * P_dot / P^3, where I = (2/5) * M * R^2"""
        if period_seconds <= 0 or p_dot <= 0:
            raise ValueError("Period and P_dot must be strictly positive.")
        i_moment = 0.4 * PulsarElectrodynamicsCore.M_NEUTRON_STAR * (PulsarElectrodynamicsCore.R_NEUTRON_STAR ** 2)
        e_dot = (4.0 * (math.pi ** 2) * i_moment * p_dot) / (period_seconds ** 3)
        return {
            "period_s": period_seconds,
            "p_dot": f"{p_dot:.6e}",
            "moment_of_inertia_kg_m2": f"{i_moment:.6e}",
            "spindown_luminosity_Watts": f"{e_dot:.6e}",
            "spindown_luminosity_erg_s": f"{e_dot * 1e7:.6e}"
        }

    @staticmethod
    def pulsar_characteristic_age_and_bfield(period_seconds: float, p_dot: float, braking_index_n: float = 3.0) -> dict:
        """tau = P / ((n - 1) * P_dot), B_surf = 3.2e19 * sqrt(P * P_dot) Gauss"""
        if period_seconds <= 0 or p_dot <= 0 or braking_index_n <= 1.0:
            raise ValueError("Invalid parameters.")
        tau_seconds = period_seconds / ((braking_index_n - 1.0) * p_dot)
        tau_years = tau_seconds / 31557600.0
        b_gauss = 3.2e19 * math.sqrt(period_seconds * p_dot)
        b_tesla = b_gauss * 1e-4
        return {
            "characteristic_age_years": round(tau_years, 2),
            "surface_b_field_Gauss": f"{b_gauss:.6e}",
            "surface_b_field_Tesla": f"{b_tesla:.6e}"
        }
