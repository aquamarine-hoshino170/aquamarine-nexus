import math

class KuttaJoukowskiLiftCore:
    @staticmethod
    def kutta_joukowski_lift_per_span(fluid_density_kg_m3: float, freestream_velocity_m_s: float, circulation_gamma_m2_s: float) -> dict:
        """L' = rho_inf * V_inf * Gamma"""
        if fluid_density_kg_m3 <= 0 or freestream_velocity_m_s <= 0:
            raise ValueError("Fluid density and flow velocity must be strictly positive.")
            
        lift_prime = fluid_density_kg_m3 * freestream_velocity_m_s * circulation_gamma_m2_s
        return {
            "fluid_density_kg_m3": fluid_density_kg_m3,
            "velocity_m_s": freestream_velocity_m_s,
            "circulation_Gamma_m2_s": circulation_gamma_m2_s,
            "lift_per_unit_span_N_m": round(lift_prime, 4)
        }

    @staticmethod
    def joukowsky_airfoil_circulation_bound(cylinder_radius_r: float, freestream_velocity_m_s: float, angle_of_attack_deg: float) -> dict:
        """Gamma = 4 * pi * V_inf * R * sin(alpha) (Kutta condition at trailing edge)"""
        if cylinder_radius_r <= 0 or freestream_velocity_m_s <= 0:
            raise ValueError("Radius and velocity must be positive.")
            
        alpha_rad = math.radians(angle_of_attack_deg)
        gamma = 4.0 * math.pi * freestream_velocity_m_s * cylinder_radius_r * math.sin(alpha_rad)
        
        return {
            "angle_of_attack_deg": angle_of_attack_deg,
            "trailing_edge_circulation_Gamma": round(gamma, 6)
        }
