import math

class SurfacePhenomenaCore:
    G_ACCEL = 9.80665

    @staticmethod
    def young_laplace_pressure(surface_tension_n_m: float, radius_r1_m: float, radius_r2_m: float = None) -> dict:
        """Delta_P = gamma * (1/R1 + 1/R2) (Spherical droplet: 2*gamma/R, Bubble: 4*gamma/R)"""
        if surface_tension_n_m <= 0 or radius_r1_m <= 0:
            raise ValueError("Surface tension and radius must be positive.")
            
        inv_r2 = (1.0 / radius_r2_m) if (radius_r2_m is not None and radius_r2_m > 0) else (1.0 / radius_r1_m)
        delta_p = surface_tension_n_m * ((1.0 / radius_r1_m) + inv_r2)
        
        return {
            "surface_tension_N_m": surface_tension_n_m,
            "radius_1_m": f"{radius_r1_m:.6e}",
            "laplace_excess_pressure_Pa": round(delta_p, 4)
        }

    @staticmethod
    def jurin_capillary_rise(surface_tension_n_m: float, contact_angle_deg: float, tube_radius_m: float, liquid_density_kg_m3: float) -> dict:
        """h = (2 * gamma * cos(theta)) / (rho * g * r)"""
        if surface_tension_n_m <= 0 or tube_radius_m <= 0 or liquid_density_kg_m3 <= 0:
            raise ValueError("Invalid parameters.")
            
        theta_rad = math.radians(contact_angle_deg)
        h = (2.0 * surface_tension_n_m * math.cos(theta_rad)) / (liquid_density_kg_m3 * SurfacePhenomenaCore.G_ACCEL * tube_radius_m)
        
        return {
            "contact_angle_deg": contact_angle_deg,
            "tube_radius_mm": round(tube_radius_m * 1e3, 4),
            "capillary_height_h_m": round(h, 6),
            "capillary_height_h_mm": round(h * 1e3, 3)
        }
