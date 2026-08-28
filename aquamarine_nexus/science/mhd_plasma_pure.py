import math

class MHDPlasmaPureCore:
    MU_0 = 1.25663706212e-6

    @staticmethod
    def alfven_wave_velocity(b_field_tesla: float, mass_density_kg_m3: float) -> dict:
        """v_A = B / sqrt(mu_0 * rho)"""
        if mass_density_kg_m3 <= 0 or b_field_tesla < 0:
            raise ValueError("Density must be strictly positive and B-field non-negative.")
        
        denom = math.sqrt(MHDPlasmaPureCore.MU_0 * mass_density_kg_m3)
        v_a = b_field_tesla / denom
        return {
            "magnetic_field_T": b_field_tesla,
            "mass_density_kg_m3": f"{mass_density_kg_m3:.6e}",
            "alfven_velocity_m_s": round(v_a, 2),
            "alfven_velocity_km_s": round(v_a / 1000.0, 3)
        }

    @staticmethod
    def magnetic_reynolds_number(characteristic_velocity_m_s: float, length_scale_m: float, electrical_conductivity_s_m: float) -> dict:
        """R_m = mu_0 * sigma * v * L"""
        if characteristic_velocity_m_s <= 0 or length_scale_m <= 0 or electrical_conductivity_s_m <= 0:
            raise ValueError("All parameters must be strictly positive.")
            
        r_m = MHDPlasmaPureCore.MU_0 * electrical_conductivity_s_m * characteristic_velocity_m_s * length_scale_m
        flux_freezing = "Flux Frozen in Fluid (Ideal MHD)" if r_m > 10.0 else ("Magnetic Diffusion Dominates (Resistive MHD)" if r_m < 0.1 else "Transition Regime")
        
        return {
            "magnetic_reynolds_number_Rm": round(r_m, 4),
            "regime": flux_freezing
        }
