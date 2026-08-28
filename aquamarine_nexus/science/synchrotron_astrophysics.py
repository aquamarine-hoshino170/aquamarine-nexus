import math

class SynchrotronAstrophysicsCore:
    C_LIGHT = 299792458.0
    E_CHARGE = 1.602176634e-19
    M_E = 9.10938356e-31
    SIGMA_T = 6.6524587158e-29  # Thomson cross-section
    EPSILON_0 = 8.8541878128e-12

    @staticmethod
    def synchrotron_critical_frequency(lorentz_gamma: float, magnetic_field_tesla: float) -> dict:
        """nu_c = (3 / (4 * pi)) * (gamma^2 * e * B) / m_e"""
        if lorentz_gamma < 1.0 or magnetic_field_tesla <= 0:
            raise ValueError("Invalid relativistic electron parameters.")
        nu_c = (3.0 / (4.0 * math.pi)) * ((lorentz_gamma ** 2) * SynchrotronAstrophysicsCore.E_CHARGE * magnetic_field_tesla) / SynchrotronAstrophysicsCore.M_E
        return {
            "lorentz_gamma": lorentz_gamma,
            "b_field_Tesla": magnetic_field_tesla,
            "critical_frequency_Hz": f"{nu_c:.6e}",
            "critical_photon_energy_eV": f"{(6.62607015e-34 * nu_c / 1.602176634e-19):.6e}"
        }

    @staticmethod
    def synchrotron_cooling_timescale(lorentz_gamma: float, magnetic_field_tesla: float) -> dict:
        """t_cool = (6 * pi * m_e * c) / (sigma_T * B^2 * gamma)"""
        if lorentz_gamma < 1.0 or magnetic_field_tesla <= 0:
            raise ValueError("Invalid parameters.")
        u_b = (magnetic_field_tesla ** 2) / (2.0 * 1.25663706212e-6)
        p_synch = (4.0 / 3.0) * SynchrotronAstrophysicsCore.SIGMA_T * SynchrotronAstrophysicsCore.C_LIGHT * ((lorentz_gamma ** 2) - 1.0) * u_b
        e_electron = lorentz_gamma * SynchrotronAstrophysicsCore.M_E * (SynchrotronAstrophysicsCore.C_LIGHT ** 2)
        t_cool = e_electron / p_synch
        return {
            "cooling_timescale_seconds": f"{t_cool:.6e}",
            "cooling_timescale_years": round(t_cool / 31557600.0, 4)
        }
