import math

class Tier1TensorSpacetimeCore:
    @staticmethod
    def schwarzschild_kretschmann_scalar(mass_m: float, radius_r: float, g_const: float = 6.67430e-11, c_light: float = 299792458.0) -> dict:
        """K = R^{\alpha\beta\gamma\delta} R_{\alpha\beta\gamma\delta} = 48 * G^2 * M^2 / (c^4 * r^6)"""
        if mass_m <= 0 or radius_r <= 0:
            raise ValueError("Mass and radius must be strictly positive.")
        
        num = 48.0 * (g_const ** 2) * (mass_m ** 2)
        denom = (c_light ** 4) * (radius_r ** 6)
        k_scalar = num / denom
        r_schwarzschild = (2.0 * g_const * mass_m) / (c_light ** 2)
        
        return {
            "mass_kg": f"{mass_m:.6e}",
            "radius_m": f"{radius_r:.6e}",
            "schwarzschild_radius_rs_m": f"{r_schwarzschild:.6e}",
            "kretschmann_invariant_K_m4": f"{k_scalar:.10e}",
            "singularity_proximity": "Inside Horizon" if radius_r < r_schwarzschild else "Outside Horizon (Asymptotically Flat)"
        }
