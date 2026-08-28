import math

class AdvancedPlasmaScreeningCore:
    EPSILON_0 = 8.8541878128e-12
    E_CHARGE = 1.602176634e-19
    K_BOLTZ = 1.380649e-23

    @staticmethod
    def debye_screening_length_multispecies(electron_density_m3: float, electron_temp_ev: float, ion_density_m3: float, ion_temp_ev: float, ion_z: int = 1) -> dict:
        """lambda_D = sqrt( epsilon_0 / ( (n_e * e^2 / k_B*T_e) + (n_i * Z^2 * e^2 / k_B*T_i) ) )"""
        if electron_density_m3 <= 0 or ion_density_m3 <= 0 or electron_temp_ev <= 0 or ion_temp_ev <= 0:
            raise ValueError("Densities and temperatures must be strictly positive.")
        
        e = AdvancedPlasmaScreeningCore.E_CHARGE
        eps0 = AdvancedPlasmaScreeningCore.EPSILON_0
        
        t_e_joules = electron_temp_ev * e
        t_i_joules = ion_temp_ev * e
        
        term_e = (electron_density_m3 * (e ** 2)) / t_e_joules
        term_i = (ion_density_m3 * ((ion_z * e) ** 2)) / t_i_joules
        
        lambda_d = math.sqrt(eps0 / (term_e + term_i))
        return {
            "electron_density_m3": f"{electron_density_m3:.4e}",
            "ion_density_m3": f"{ion_density_m3:.4e}",
            "combined_debye_length_m": f"{lambda_d:.6e}"
        }

    @staticmethod
    def plasma_coupling_parameter(ion_density_m3: float, ion_temp_ev: float, ion_z: int = 1) -> dict:
        """Gamma = (Z^2 * e^2 / (4 * pi * epsilon_0 * a)) / (k_B * T_i), where a = (3 / (4*pi*n))^(1/3)"""
        if ion_density_m3 <= 0 or ion_temp_ev <= 0:
            raise ValueError("Density and temperature must be positive.")
        
        e = AdvancedPlasmaScreeningCore.E_CHARGE
        eps0 = AdvancedPlasmaScreeningCore.EPSILON_0
        wigner_seitz_radius = (3.0 / (4.0 * math.pi * ion_density_m3)) ** (1.0 / 3.0)
        
        coulomb_energy = ((ion_z * e) ** 2) / (4.0 * math.pi * eps0 * wigner_seitz_radius)
        thermal_energy = ion_temp_ev * e
        gamma = coulomb_energy / thermal_energy
        
        regime = "Strongly Coupled (Liquid/Crystal)" if gamma >= 1.0 else "Weakly Coupled (Ideal Gas Plasma)"
        return {
            "wigner_seitz_radius_m": f"{wigner_seitz_radius:.6e}",
            "coupling_parameter_gamma": round(gamma, 6),
            "plasma_regime": regime
        }
