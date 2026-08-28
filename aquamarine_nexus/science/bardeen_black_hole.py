import math

class BardeenBlackHoleCore:
    G_CONST = 6.67430e-11
    C_LIGHT = 299792458.0

    @staticmethod
    def bardeen_horizon_equation(mass_kg: float, magnetic_charge_g_meters: float, radius_m: float) -> dict:
        """f(r) = 1 - (2 * G * M * r^2) / (c^2 * (r^2 + g^2)^(3/2))"""
        if radius_m <= 0 or mass_kg <= 0:
            raise ValueError("Radius and mass must be strictly positive.")
        g = BardeenBlackHoleCore.G_CONST
        c = BardeenBlackHoleCore.C_LIGHT
        rg = (g * mass_kg) / (c ** 2)
        
        denom = (radius_m ** 2 + magnetic_charge_g_meters ** 2) ** 1.5
        f_r = 1.0 - (2.0 * rg * (radius_m ** 2)) / denom
        
        # Critical magnetic charge bound: g_crit = (4/(3*sqrt(3))) * rg approx 0.7698 * rg
        g_crit = (4.0 / (3.0 * math.sqrt(3.0))) * rg
        
        return {
            "radius_m": f"{radius_m:.6e}",
            "metric_lapse_f_r": round(f_r, 6),
            "critical_charge_bound_meters": f"{g_crit:.6e}",
            "is_regular_black_hole": magnetic_charge_g_meters <= g_crit
        }
