import math

class BlackHoleShadowCore:
    G_CONST = 6.67430e-11
    C_LIGHT = 299792458.0

    @staticmethod
    def schwarzschild_shadow_radius(mass_kg: float) -> dict:
        """R_shadow = 3 * sqrt(3) * G * M / c^2 approx 5.196 * r_g"""
        rg = (BlackHoleShadowCore.G_CONST * mass_kg) / (BlackHoleShadowCore.C_LIGHT ** 2)
        r_shadow = 3.0 * math.sqrt(3.0) * rg
        return {
            "gravitational_radius_rg_m": f"{rg:.6e}",
            "shadow_radius_meters": f"{r_shadow:.6e}",
            "shadow_impact_parameter_rg_units": round(3.0 * math.sqrt(3.0), 4)
        }

    @staticmethod
    def kerr_shadow_extremal_axes(spin_param_a_star: float, inclination_deg: float = 90.0) -> dict:
        """Equatorial horizontal radius shift & vertical elongation for Kerr shadow"""
        if spin_param_a_star < 0 or spin_param_a_star > 1.0:
            raise ValueError("Spin parameter must be within [0, 1].")
        inc_rad = math.radians(inclination_deg)
        sin_i = math.sin(inc_rad)
        
        # Retrograde & prograde impact bounds
        xi_retro = - (spin_param_a_star + 6.0)
        xi_pro = 3.0 * (3.0**0.5) - spin_param_a_star if spin_param_a_star < 1.0 else 2.0
        horizontal_diameter = (abs(xi_retro) + abs(xi_pro)) * sin_i
        
        return {
            "spin_a_star": spin_param_a_star,
            "inclination_deg": inclination_deg,
            "horizontal_diameter_rg": round(horizontal_diameter, 4),
            "shadow_distortion_asymmetry": round(abs(xi_retro) - abs(xi_pro), 4)
        }
