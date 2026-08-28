import math

class MossbauerSpectroscopyCore:
    C_LIGHT = 299792458.0
    K_BOLTZ = 1.380649e-23
    U_AMU_KG = 1.66053906660e-27
    E_CHARGE = 1.602176634e-19

    @staticmethod
    def nuclear_recoil_energy(gamma_energy_kev: float, nucleus_mass_amu: float) -> dict:
        """E_R = E_gamma^2 / (2 * M * c^2)"""
        if gamma_energy_kev <= 0 or nucleus_mass_amu <= 0:
            raise ValueError("Gamma energy and nuclear mass must be positive.")
            
        e_gamma_j = gamma_energy_kev * 1e3 * MossbauerSpectroscopyCore.E_CHARGE
        m_kg = nucleus_mass_amu * MossbauerSpectroscopyCore.U_AMU_KG
        c = MossbauerSpectroscopyCore.C_LIGHT
        
        e_recoil_j = (e_gamma_j ** 2) / (2.0 * m_kg * (c ** 2))
        e_recoil_ev = e_recoil_j / MossbauerSpectroscopyCore.E_CHARGE
        
        return {
            "gamma_energy_keV": gamma_energy_kev,
            "nucleus_mass_amu": nucleus_mass_amu,
            "recoil_energy_eV": round(e_recoil_ev, 6),
            "recoil_energy_meV": round(e_recoil_ev * 1000.0, 4)
        }

    @staticmethod
    def lamb_mossbauer_recoil_free_fraction(recoil_energy_ev: float, debye_temp_k: float, temp_k: float) -> dict:
        """f = exp( - (3 * E_R) / (2 * k_B * Theta_D) * (1 + 4 * (T / Theta_D)^2 * integral) ) (Low T limit: exp(-3*E_R / 2*k_B*Theta_D))"""
        if recoil_energy_ev < 0 or debye_temp_k <= 0 or temp_k <= 0:
            raise ValueError("Physical parameters must be valid.")
            
        e_r_j = recoil_energy_ev * MossbauerSpectroscopyCore.E_CHARGE
        kb = MossbauerSpectroscopyCore.K_BOLTZ
        
        # Zero-point motion low-temperature approximation
        exponent = - (3.0 * e_r_j) / (2.0 * kb * debye_temp_k) * (1.0 + (math.pi ** 2 / 3.0) * ((temp_k / debye_temp_k) ** 2))
        f_fraction = math.exp(exponent) if exponent > -700 else 0.0
        
        return {
            "temperature_K": temp_k,
            "debye_temperature_ThetaD_K": debye_temp_k,
            "recoil_free_fraction_f": round(f_fraction, 6),
            "mossbauer_emission_detectable": f_fraction > 1e-4
        }
