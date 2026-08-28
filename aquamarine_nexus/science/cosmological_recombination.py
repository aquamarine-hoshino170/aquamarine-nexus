import math

class CosmologicalRecombinationCore:
    K_BOLTZ = 1.380649e-23
    H_PLANCK = 6.62607015e-34
    M_ELECTRON = 9.10938356e-31
    EV_TO_JOULE = 1.602176634e-19

    @staticmethod
    def saha_hydrogen_ionization_fraction(baryon_density_m3: float, temp_kelvin: float) -> dict:
        """(x_e^2) / (1 - x_e) = (1 / n_b) * ( (m_e * k_B * T) / (2 * pi * hbar^2) )^(3/2) * exp(-E_ion / k_B*T)"""
        if baryon_density_m3 <= 0 or temp_kelvin <= 0:
            raise ValueError("Density and temperature must be positive.")
        
        hbar = CosmologicalRecombinationCore.H_PLANCK / (2.0 * math.pi)
        e_ion = 13.605693 * CosmologicalRecombinationCore.EV_TO_JOULE
        kb_t = CosmologicalRecombinationCore.K_BOLTZ * temp_kelvin
        
        thermal_factor = ((CosmologicalRecombinationCore.M_ELECTRON * kb_t) / (2.0 * math.pi * (hbar ** 2))) ** 1.5
        boltzmann_factor = math.exp(-e_ion / kb_t) if (e_ion / kb_t) < 700 else 0.0
        
        rhs = (thermal_factor / baryon_density_m3) * boltzmann_factor
        
        # Solving x^2 / (1 - x) = rhs  =>  x^2 + rhs*x - rhs = 0
        disc = (rhs ** 2) + (4.0 * rhs)
        x_e = (-rhs + math.sqrt(disc)) / 2.0
        
        return {
            "temperature_K": temp_kelvin,
            "baryon_density_m3": f"{baryon_density_m3:.4e}",
            "ionization_fraction_x_e": round(min(x_e, 1.0), 6),
            "neutral_fraction": round(max(0.0, 1.0 - x_e), 6)
        }
