import math

class SuperconductivityCore:
    """BCS Superconductivity & London Electrodynamics Engine"""

    MU_0 = 4.0 * math.pi * 1e-7
    M_ELECTRON = 9.10938356e-31
    Q_ELEM = 1.602176634e-19
    K_BOLTZ = 1.380649e-23
    EV_TO_JOULE = 1.602176634e-19

    @staticmethod
    def london_penetration_depth(superconducting_density_m3: float) -> dict:
        """
        Calculates London Penetration Depth: lambda_L = sqrt( m_e / (mu_0 * n_s * e^2) )
        """
        if superconducting_density_m3 <= 0:
            raise ValueError("Superconducting carrier density n_s must be strictly positive.")

        m_e = SuperconductivityCore.M_ELECTRON
        mu_0 = SuperconductivityCore.MU_0
        e = SuperconductivityCore.Q_ELEM

        lambda_l = math.sqrt(m_e / (mu_0 * superconducting_density_m3 * (e ** 2)))
        return {
            "superconducting_density_m3": superconducting_density_m3,
            "london_penetration_depth_m": f"{lambda_l:.6e}",
            "depth_nanometers": round(lambda_l * 1e9, 2)
        }

    @staticmethod
    def bcs_energy_gap_zero_t(critical_temp_k: float) -> dict:
        """
        Computes BCS superconducting energy gap at T = 0 K:
        Delta(0) = 1.764 * k_B * T_c
        """
        if critical_temp_k <= 0:
            raise ValueError("Critical temperature T_c must be strictly positive.")

        kb = SuperconductivityCore.K_BOLTZ
        delta_joules = 1.764 * kb * critical_temp_k
        delta_mev = (delta_joules / SuperconductivityCore.EV_TO_JOULE) * 1000.0

        return {
            "critical_temp_K": critical_temp_k,
            "energy_gap_Joules": f"{delta_joules:.6e}",
            "energy_gap_meV": round(delta_mev, 4)
        }

    @staticmethod
    def critical_magnetic_field(t_kelvin: float, tc_kelvin: float, b_c0_tesla: float) -> dict:
        """
        Computes thermodynamic critical field: B_c(T) = B_c(0) * (1 - (T / T_c)^2)
        """
        if tc_kelvin <= 0 or b_c0_tesla < 0:
            raise ValueError("T_c and B_c(0) must be positive.")

        if t_kelvin >= tc_kelvin:
            return {"temperature_K": t_kelvin, "is_superconducting": False, "critical_field_Tesla": 0.0}

        ratio = (t_kelvin / tc_kelvin) ** 2
        b_c = b_c0_tesla * (1.0 - ratio)

        return {
            "temperature_K": t_kelvin,
            "critical_temp_K": tc_kelvin,
            "is_superconducting": True,
            "critical_field_Tesla": round(b_c, 5)
        }
