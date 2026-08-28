class RealGasCore:
    """Non-Ideal Gas Thermodynamics & Van der Waals Equations of State"""

    R_GAS = 8.314462618

    @staticmethod
    def van_der_waals_pressure(temp_k: float, molar_volume_m3_mol: float, a_param: float, b_param: float) -> dict:
        """
        Computes real gas pressure:
        P = (R * T) / (V_m - b) - a / (V_m^2)
        """
        r = RealGasCore.R_GAS
        if molar_volume_m3_mol <= b_param:
            raise ValueError("Molar volume V_m must be strictly greater than co-volume b.")

        p_ideal = (r * temp_k) / molar_volume_m3_mol
        p_real = (r * temp_k) / (molar_volume_m3_mol - b_param) - (a_param / (molar_volume_m3_mol ** 2))
        z_factor = (p_real * molar_volume_m3_mol) / (r * temp_k)

        return {
            "temperature_K": temp_k,
            "molar_volume": molar_volume_m3_mol,
            "ideal_pressure_Pa": f"{p_ideal:.4e}",
            "real_pressure_Pa": f"{p_real:.4e}",
            "compressibility_Z": round(z_factor, 5)
        }
