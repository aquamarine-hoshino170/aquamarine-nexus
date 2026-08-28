class ThermoelectricityCore:
    @staticmethod
    def thermoelectric_figure_of_merit_zt(seebeck_s_v_k: float, electrical_cond_sigma: float, thermal_cond_kappa: float, temp_k: float) -> dict:
        """ZT = (S^2 * sigma * T) / kappa"""
        if thermal_cond_kappa <= 0 or temp_k <= 0:
            raise ValueError("Thermal conductivity and temperature must be strictly positive.")
        power_factor = (seebeck_s_v_k ** 2) * electrical_cond_sigma
        zt = (power_factor * temp_k) / thermal_cond_kappa
        return {"power_factor_W_m_K2": f"{power_factor:.6e}", "temperature_K": temp_k, "dimensionless_figure_of_merit_ZT": round(zt, 4)}

    @staticmethod
    def peltier_heat_flux(seebeck_s_v_k: float, current_amperes: float, temp_k: float) -> dict:
        """Pi = S * T, Q_dot = Pi * I = S * T * I (Kelvin 1st Relation)"""
        peltier_pi = seebeck_s_v_k * temp_k
        q_dot = peltier_pi * current_amperes
        return {"peltier_coefficient_Volts": round(peltier_pi, 6), "heat_flux_Watts": round(q_dot, 6)}
