import math

class DarkMatterHaloCore:
    """Astrophysical NFW Halo Profiles & Jeans Gravitational Collapse"""

    G_CONST = 6.67430e-11
    K_BOLTZ = 1.380649e-23
    M_PROTON = 1.67262192369e-27

    @staticmethod
    def nfw_density_profile(radius_kpc: float, scale_radius_rs_kpc: float, rho_0_msun_kpc3: float) -> dict:
        """
        Navarro-Frenk-White (NFW) Dark Matter Density Profile:
        rho(r) = rho_0 / [ (r / R_s) * (1 + r / R_s)^2 ]
        """
        if radius_kpc <= 0 or scale_radius_rs_kpc <= 0:
            raise ValueError("Radius and scale radius must be strictly positive.")

        x = radius_kpc / scale_radius_rs_kpc
        rho_r = rho_0_msun_kpc3 / (x * ((1.0 + x) ** 2))

        return {
            "radius_kpc": radius_kpc,
            "dimensionless_radius_x": round(x, 4),
            "density_rho_r": f"{rho_r:.6e}"
        }

    @staticmethod
    def jeans_instability_mass(density_kg_m3: float, gas_temp_k: float, mean_molecular_weight: float = 1.0) -> dict:
        """
        Computes Jeans Length (lambda_J) and Jeans Critical Mass (M_J) for gravitational collapse:
        c_s = sqrt( (k_B * T) / (mu * m_p) )
        lambda_J = sqrt( (pi * c_s^2) / (G * rho) )
        M_J = (pi / 6) * rho * lambda_J^3
        """
        if density_kg_m3 <= 0 or gas_temp_k <= 0:
            raise ValueError("Density and Temperature must be positive.")

        g = DarkMatterHaloCore.G_CONST
        kb = DarkMatterHaloCore.K_BOLTZ
        mp = DarkMatterHaloCore.M_PROTON

        # Sound speed c_s
        c_sound = math.sqrt((kb * gas_temp_k) / (mean_molecular_weight * mp))
        
        # Jeans length lambda_J
        lambda_j = math.sqrt((math.pi * (c_sound ** 2)) / (g * density_kg_m3))
        
        # Jeans mass M_J
        m_jeans = (math.pi / 6.0) * density_kg_m3 * (lambda_j ** 3)
        solar_mass = 1.989e30

        return {
            "sound_speed_m_s": round(c_sound, 2),
            "jeans_length_m": f"{lambda_j:.6e}",
            "jeans_mass_kg": f"{m_jeans:.6e}",
            "jeans_mass_solar_units": f"{m_jeans / solar_mass:.4e}"
        }
