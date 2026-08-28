import math

class NonSteadyDiffusionFickCore:
    @staticmethod
    def transient_concentration_profile(c_surface: float, c_bulk: float, distance_x_m: float, time_s: float, diffusion_coeff_m2_s: float) -> dict:
        """C(x, t) = C_s - (C_s - C_0) * erf( x / (2 * sqrt(D * t)) )"""
        if time_s <= 0 or diffusion_coeff_m2_s <= 0 or distance_x_m < 0:
            raise ValueError("Time and diffusion coefficient must be strictly positive, distance non-negative.")
            
        z = distance_x_m / (2.0 * math.sqrt(diffusion_coeff_m2_s * time_s))
        erf_val = math.erf(z)
        
        c_xt = c_surface - (c_surface - c_bulk) * erf_val
        penetration_depth = 2.0 * math.sqrt(diffusion_coeff_m2_s * time_s)
        
        return {
            "diffusion_time_s": time_s,
            "distance_x_um": round(distance_x_m * 1e6, 3),
            "characteristic_diffusion_length_um": round(penetration_depth * 1e6, 3),
            "dimensionless_argument_z": round(z, 6),
            "concentration_at_x_t": round(c_xt, 6)
        }
