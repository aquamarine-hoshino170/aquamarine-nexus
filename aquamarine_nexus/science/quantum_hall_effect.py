class QuantumHallEffectCore:
    H_PLANCK = 6.62607015e-34
    E_CHARGE = 1.602176634e-19

    @staticmethod
    def von_klitzing_hall_resistance(filling_factor_nu: int) -> dict:
        """R_H = h / (nu * e^2) = R_K / nu"""
        if filling_factor_nu <= 0:
            raise ValueError("Filling factor integer nu must be >= 1.")
            
        r_k = QuantumHallEffectCore.H_PLANCK / (QuantumHallEffectCore.E_CHARGE ** 2)
        r_h = r_k / filling_factor_nu
        
        return {
            "filling_factor_nu": filling_factor_nu,
            "von_klitzing_constant_R_K_Ohms": round(r_k, 4),
            "hall_plateau_resistance_Ohms": round(r_h, 6)
        }

    @staticmethod
    def landau_level_degeneracy_density(magnetic_field_tesla: float) -> dict:
        """n_B = (e * B) / h"""
        if magnetic_field_tesla <= 0:
            raise ValueError("Magnetic field must be positive.")
            
        n_b = (QuantumHallEffectCore.E_CHARGE * magnetic_field_tesla) / QuantumHallEffectCore.H_PLANCK
        flux_quantum_phi0 = QuantumHallEffectCore.H_PLANCK / QuantumHallEffectCore.E_CHARGE
        
        return {
            "magnetic_field_Tesla": magnetic_field_tesla,
            "magnetic_flux_quantum_Wb": f"{flux_quantum_phi0:.6e}",
            "degeneracy_per_unit_area_m2": f"{n_b:.6e}"
        }
