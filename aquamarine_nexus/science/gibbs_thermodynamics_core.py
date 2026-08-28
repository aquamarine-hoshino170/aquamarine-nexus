class GibbsThermodynamicsCore:
    @staticmethod
    def gibbs_free_energy_change(delta_h_joules: float, delta_s_joules_per_k: float, temp_k: float) -> dict:
        """Delta_G = Delta_H - T * Delta_S"""
        if temp_k <= 0: raise ValueError("Temperature must be strictly positive.")
        delta_g = delta_h_joules - (temp_k * delta_s_joules_per_k)
        
        spontaneity = "Spontaneous (Exergonic)" if delta_g < 0 else ("Non-spontaneous (Endergonic)" if delta_g > 0 else "Equilibrium")
        return {
            "delta_H_Joules": delta_h_joules,
            "delta_S_J_K": delta_s_joules_per_k,
            "temperature_K": temp_k,
            "delta_G_Joules": round(delta_g, 4),
            "process_state": spontaneity
        }

    @staticmethod
    def gibbs_phase_rule(num_components_c: int, num_phases_p: int) -> dict:
        """Degrees of freedom: F = C - P + 2"""
        if num_components_c <= 0 or num_phases_p <= 0:
            raise ValueError("Components and phases must be >= 1.")
        degrees_of_freedom_f = num_components_c - num_phases_p + 2
        return {
            "components_C": num_components_c,
            "phases_P": num_phases_p,
            "degrees_of_freedom_F": degrees_of_freedom_f,
            "is_system_invariant": degrees_of_freedom_f == 0
        }
