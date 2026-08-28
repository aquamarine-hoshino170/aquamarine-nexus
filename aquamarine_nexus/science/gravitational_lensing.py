import math

class GravitationalLensingCore:
    G_CONST = 6.67430e-11
    C_LIGHT = 299792458.0
    MPC_METERS = 3.085677581e22

    @staticmethod
    def einstein_radius_angle(lens_mass_kg: float, d_l_mpc: float, d_s_mpc: float, d_ls_mpc: float) -> dict:
        """theta_E = sqrt( (4 * G * M / c^2) * (D_ls / (D_l * D_s)) )"""
        if lens_mass_kg <= 0 or d_l_mpc <= 0 or d_s_mpc <= 0 or d_ls_mpc <= 0:
            raise ValueError("Invalid astrophysical distances or lens mass.")
        d_l = d_l_mpc * GravitationalLensingCore.MPC_METERS
        d_s = d_s_mpc * GravitationalLensingCore.MPC_METERS
        d_ls = d_ls_mpc * GravitationalLensingCore.MPC_METERS

        theta_e_rad = math.sqrt((4.0 * GravitationalLensingCore.G_CONST * lens_mass_kg / (GravitationalLensingCore.C_LIGHT ** 2)) * (d_ls / (d_l * d_s)))
        theta_e_arcsec = math.degrees(theta_e_rad) * 3600.0
        return {
            "einstein_radius_radians": f"{theta_e_rad:.6e}",
            "einstein_radius_arcsec": round(theta_e_arcsec, 4)
        }

    @staticmethod
    def point_mass_lensing_magnification(impact_param_u: float) -> dict:
        """mu_tot = (u^2 + 2) / (u * sqrt(u^2 + 4))"""
        if impact_param_u <= 0:
            raise ValueError("Impact parameter u = theta / theta_E must be strictly positive.")
        u2 = impact_param_u ** 2
        mu_plus = (u2 + 2.0 + impact_param_u * math.sqrt(u2 + 4.0)) / (2.0 * impact_param_u * math.sqrt(u2 + 4.0))
        mu_minus = (u2 + 2.0 - impact_param_u * math.sqrt(u2 + 4.0)) / (2.0 * impact_param_u * math.sqrt(u2 + 4.0))
        mu_tot = (u2 + 2.0) / (impact_param_u * math.sqrt(u2 + 4.0))
        return {
            "impact_parameter_u": impact_param_u,
            "magnification_image_1": round(mu_plus, 4),
            "magnification_image_2": round(abs(mu_minus), 4),
            "total_magnification": round(mu_tot, 4)
        }
