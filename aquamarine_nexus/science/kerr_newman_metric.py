import math

class KerrNewmanCore:
    G_CONST = 6.67430e-11
    C_LIGHT = 299792458.0
    EPSILON_0 = 8.8541878128e-12

    @staticmethod
    def kerr_newman_radii(mass_kg: float, spin_a_meters: float, electric_charge_coulombs: float, theta_rad: float = 1.5707963) -> dict:
        """r_plus = M + sqrt(M^2 - a^2 - r_Q^2), r_ergo = M + sqrt(M^2 - a^2*cos^2(theta) - r_Q^2)"""
        if mass_kg <= 0:
            raise ValueError("Mass must be strictly positive.")
        g = KerrNewmanCore.G_CONST
        c = KerrNewmanCore.C_LIGHT
        eps0 = KerrNewmanCore.EPSILON_0
        
        m_geom = (g * mass_kg) / (c ** 2)
        r_q_sq = (g * (electric_charge_coulombs ** 2)) / (4.0 * math.pi * eps0 * (c ** 4))
        
        disc_horizon = (m_geom ** 2) - (spin_a_meters ** 2) - r_q_sq
        if disc_horizon < 0:
            return {"status": "Naked Singularity (No Horizon)", "discriminant": round(disc_horizon, 6)}
        
        r_plus = m_geom + math.sqrt(disc_horizon)
        r_minus = m_geom - math.sqrt(disc_horizon)
        
        disc_ergo = (m_geom ** 2) - ((spin_a_meters * math.cos(theta_rad)) ** 2) - r_q_sq
        r_ergo = m_geom + math.sqrt(disc_ergo) if disc_ergo >= 0 else None
        
        return {
            "geometric_mass_m": f"{m_geom:.6e}",
            "outer_event_horizon_r_plus_m": f"{r_plus:.6e}",
            "inner_cauchy_horizon_r_minus_m": f"{r_minus:.6e}",
            "outer_ergosphere_radius_m": f"{r_ergo:.6e}" if r_ergo else "Undefined",
            "is_extremal": abs(disc_horizon) < 1e-12
        }
