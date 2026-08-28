import math

class AccretionDisksCore:
    G_CONST = 6.67430e-11
    C_LIGHT = 299792458.0
    SIGMA_SB = 5.670374419e-8

    @staticmethod
    def shakura_sunyaev_effective_temp(black_hole_mass_kg: float, mdot_kg_s: float, radius_m: float) -> dict:
        """T_eff(r) = [ (3 * G * M * M_dot) / (8 * pi * sigma_SB * r^3) * (1 - sqrt(R_in / r)) ]^(1/4)"""
        if black_hole_mass_kg <= 0 or mdot_kg_s <= 0 or radius_m <= 0:
            raise ValueError("Mass, accretion rate, and radius must be positive.")
        r_isco = (6.0 * AccretionDisksCore.G_CONST * black_hole_mass_kg) / (AccretionDisksCore.C_LIGHT ** 2)
        if radius_m <= r_isco:
            return {"radius_m": radius_m, "r_isco_m": r_isco, "effective_temp_K": 0.0, "status": "Inside ISCO"}
        
        factor = (3.0 * AccretionDisksCore.G_CONST * black_hole_mass_kg * mdot_kg_s) / (8.0 * math.pi * AccretionDisksCore.SIGMA_SB * (radius_m ** 3))
        boundary_term = 1.0 - math.sqrt(r_isco / radius_m)
        t_eff = (factor * boundary_term) ** 0.25
        return {
            "radius_m": f"{radius_m:.6e}",
            "r_isco_m": f"{r_isco:.6e}",
            "effective_temp_K": round(t_eff, 2)
        }

    @staticmethod
    def eddington_accretion_rate(mass_kg: float, radiative_efficiency_eta: float = 0.1) -> dict:
        """M_dot_Edd = L_Edd / (eta * c^2) = (4 * pi * G * M * m_p * c) / (sigma_T * eta * c^2)"""
        if mass_kg <= 0 or radiative_efficiency_eta <= 0:
            raise ValueError("Mass and efficiency must be strictly positive.")
        l_edd = (4.0 * math.pi * AccretionDisksCore.G_CONST * mass_kg * 1.67262192369e-27 * AccretionDisksCore.C_LIGHT) / 6.6524587158e-29
        mdot_edd = l_edd / (radiative_efficiency_eta * (AccretionDisksCore.C_LIGHT ** 2))
        return {
            "eddington_luminosity_Watts": f"{l_edd:.6e}",
            "eddington_accretion_rate_kg_s": f"{mdot_edd:.6e}",
            "eddington_accretion_rate_msun_yr": round(mdot_edd * 31557600.0 / 1.989e30, 6)
        }
