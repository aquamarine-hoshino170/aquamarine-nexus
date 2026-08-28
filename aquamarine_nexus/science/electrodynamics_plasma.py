import math

class ElectrodynamicsPlasmaCore:
    EPSILON_0 = 8.8541878128e-12
    E_CHARGE = 1.602176634e-19
    M_ELECTRON = 9.10938356e-31
    C_LIGHT = 299792458.0

    @staticmethod
    def plasma_frequency(electron_density_m3: float) -> dict:
        """omega_pe = sqrt( (n_e * e^2) / (epsilon_0 * m_e) )"""
        if electron_density_m3 <= 0: raise ValueError("Density must be positive.")
        w_pe = math.sqrt((electron_density_m3 * (ElectrodynamicsPlasmaCore.E_CHARGE ** 2)) / (ElectrodynamicsPlasmaCore.EPSILON_0 * ElectrodynamicsPlasmaCore.M_ELECTRON))
        return {"electron_density_m3": electron_density_m3, "plasma_frequency_rad_s": f"{w_pe:.6e}", "plasma_frequency_Hz": f"{w_pe / (2.0 * math.pi):.6e}"}

    @staticmethod
    def cyclotron_frequency(magnetic_field_tesla: float) -> dict:
        """omega_c = (e * B) / m_e"""
        if magnetic_field_tesla < 0: raise ValueError("B field must be non-negative.")
        w_c = (ElectrodynamicsPlasmaCore.E_CHARGE * magnetic_field_tesla) / ElectrodynamicsPlasmaCore.M_ELECTRON
        return {"magnetic_field_Tesla": magnetic_field_tesla, "cyclotron_frequency_rad_s": f"{w_c:.6e}", "cyclotron_frequency_Hz": f"{w_c / (2.0 * math.pi):.6e}"}

    @staticmethod
    def radiation_pressure_em(pointing_flux_w_m2: float, is_perfect_reflector: bool = False) -> dict:
        """P = (1 + R) * (S / c)"""
        if pointing_flux_w_m2 < 0: raise ValueError("Poynting flux must be non-negative.")
        factor = 2.0 if is_perfect_reflector else 1.0
        p_rad = factor * (pointing_flux_w_m2 / ElectrodynamicsPlasmaCore.C_LIGHT)
        return {"poynting_flux_W_m2": pointing_flux_w_m2, "is_reflection": is_perfect_reflector, "radiation_pressure_Pascals": f"{p_rad:.6e}"}
