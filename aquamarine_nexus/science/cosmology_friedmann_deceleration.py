class CosmologyFriedmannDecelerationCore:
    @staticmethod
    def cosmological_deceleration_parameter(omega_matter: float, omega_radiation: float, omega_dark_energy: float) -> dict:
        """q_0 = 0.5 * Omega_m + Omega_r - Omega_Lambda"""
        if omega_matter < 0 or omega_radiation < 0 or omega_dark_energy < 0:
            raise ValueError("Density parameters must be non-negative.")
            
        omega_total = omega_matter + omega_radiation + omega_dark_energy
        q0 = (0.5 * omega_matter) + omega_radiation - omega_dark_energy
        
        return {
            "Omega_matter": omega_matter,
            "Omega_radiation": omega_radiation,
            "Omega_Lambda": omega_dark_energy,
            "Omega_total": round(omega_total, 4),
            "deceleration_parameter_q0": round(q0, 4),
            "cosmic_expansion_state": "Accelerating Expansion (Dark Energy Dominant)" if q0 < 0 else ("Decelerating Expansion" if q0 > 0 else "Constant Expansion")
        }
