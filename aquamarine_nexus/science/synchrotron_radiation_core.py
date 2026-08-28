import math

class SynchrotronRadiationCore:
    E_CHARGE = 1.602176634e-19
    EPSILON_0 = 8.8541878128e-12
    C_LIGHT = 299792458.0
    M_ELECTRON = 9.10938356e-31

    @staticmethod
    def synchrotron_total_emitted_power(relativistic_gamma: float, bending_radius_rho_m: float) -> dict:
        """P = (e^2 * c * gamma^4) / (6 * pi * epsilon_0 * rho^2)"""
        if relativistic_gamma <= 1.0 or bending_radius_rho_m <= 0:
            raise ValueError("Gamma must be > 1 and radius strictly positive.")
            
        e = SynchrotronRadiationCore.E_CHARGE
        eps0 = SynchrotronRadiationCore.EPSILON_0
        c = SynchrotronRadiationCore.C_LIGHT
        
        num = (e ** 2) * c * (relativistic_gamma ** 4)
        denom = 6.0 * math.pi * eps0 * (bending_radius_rho_m ** 2)
        power_watts = num / denom
        
        return {
            "lorentz_gamma": relativistic_gamma,
            "bending_radius_meters": bending_radius_rho_m,
            "total_power_Watts": f"{power_watts:.6e}",
            "total_power_keV_s": f"{(power_watts / (e * 1e3)):.6e}"
        }

    @staticmethod
    def synchrotron_critical_photon_energy(relativistic_gamma: float, bending_radius_rho_m: float) -> dict:
        """omega_c = (3 * c * gamma^3) / (2 * rho), E_c = hbar * omega_c"""
        if relativistic_gamma <= 1.0 or bending_radius_rho_m <= 0:
            raise ValueError("Invalid parameters.")
            
        c = SynchrotronRadiationCore.C_LIGHT
        h_bar = 1.054571817e-34
        e = SynchrotronRadiationCore.E_CHARGE
        
        omega_c = (3.0 * c * (relativistic_gamma ** 3)) / (2.0 * bending_radius_rho_m)
        e_c_joules = h_bar * omega_c
        e_c_ev = e_c_joules / e
        
        return {
            "critical_angular_frequency_rad_s": f"{omega_c:.6e}",
            "critical_photon_energy_eV": round(e_c_ev, 4),
            "critical_photon_energy_keV": round(e_c_ev / 1000.0, 4)
        }
