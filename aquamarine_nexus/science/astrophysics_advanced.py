import math

class AstrophysicsAdvancedCore:
    G_CONST = 6.67430e-11
    C_LIGHT = 299792458.0
    M_SUN = 1.989e30
    M_PROTON = 1.67262192369e-27
    H_BAR = 1.054571817e-34

    @staticmethod
    def chandrasekhar_mass_limit(mu_e: float = 2.0) -> dict:
        """M_ch = (omega_3^0 / mu_e^2) * sqrt(3 * pi) / 2 * (hbar*c / G)^(3/2) / m_p^2"""
        if mu_e <= 0: raise ValueError("mu_e must be positive.")
        hbar_c_over_g = (AstrophysicsAdvancedCore.H_BAR * AstrophysicsAdvancedCore.C_LIGHT) / AstrophysicsAdvancedCore.G_CONST
        m_planck_cubed = hbar_c_over_g ** 1.5
        m_ch_kg = 0.77 * (1.0 / (mu_e ** 2)) * m_planck_cubed / (AstrophysicsAdvancedCore.M_PROTON ** 2)
        return {"mean_molecular_weight_mu_e": mu_e, "chandrasekhar_mass_kg": f"{m_ch_kg:.6e}", "chandrasekhar_mass_msun": round(m_ch_kg / AstrophysicsAdvancedCore.M_SUN, 4)}

    @staticmethod
    def kerr_isco_radius(black_hole_mass_kg: float, spin_param_a_star: float) -> dict:
        """Innermost Stable Circular Orbit (ISCO) for prograde Kerr black hole"""
        if spin_param_a_star < 0 or spin_param_a_star > 1.0 or black_hole_mass_kg <= 0: raise ValueError("Invalid parameters.")
        rg = (AstrophysicsAdvancedCore.G_CONST * black_hole_mass_kg) / (AstrophysicsAdvancedCore.C_LIGHT ** 2)
        z1 = 1.0 + ((1.0 - spin_param_a_star**2)**(1/3)) * (((1.0 + spin_param_a_star)**(1/3)) + ((1.0 - spin_param_a_star)**(1/3)))
        z2 = math.sqrt(3.0 * (spin_param_a_star**2) + z1**2)
        r_isco = rg * (3.0 + z2 - math.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2)))
        return {"black_hole_mass_kg": black_hole_mass_kg, "spin_parameter_a_star": spin_param_a_star, "r_isco_meters": f"{r_isco:.6e}", "r_isco_rg_units": round(r_isco / rg, 4)}
