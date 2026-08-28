import math

class GamowNucleosynthesisCore:
    K_BOLTZ = 1.380649e-23
    EV_TO_JOULE = 1.602176634e-19

    @staticmethod
    def gamow_energy_peak(z1: int, z2: int, reduced_mass_amu: float, temp_kelvin: float) -> dict:
        """
        E_0 = ( (b * k_B * T) / 2 )^(2/3), where b = pi * alpha * z1 * z2 * sqrt(2 * m * c^2)
        Delta_E0 = 4 / sqrt(3) * (E_0 * k_B * T)^(1/2)
        """
        if z1 <= 0 or z2 <= 0 or reduced_mass_amu <= 0 or temp_kelvin <= 0:
            raise ValueError("Invalid nuclear parameters.")
        
        t9 = temp_kelvin / 1e9
        e0_kev = 1.22 * ((z1**2 * z2**2 * reduced_mass_amu * (t9**2)) ** (1.0 / 3.0))
        delta_e0_kev = 0.749 * ((z1**2 * z2**2 * reduced_mass_amu * (t9**5)) ** (1.0 / 6.0))

        return {
            "temp_T9": round(t9, 4),
            "gamow_peak_energy_keV": round(e0_kev, 4),
            "gamow_window_width_keV": round(delta_e0_kev, 4)
        }

    @staticmethod
    def tunneling_probability_wkb(energy_kev: float, z1: int, z2: int, reduced_mass_amu: float) -> dict:
        """P = exp( - 2 * pi * eta ), Sommerfeld eta = z1*z2*e^2 / (hbar * v)"""
        if energy_kev <= 0:
            raise ValueError("Energy must be strictly positive.")
        
        eg_kev = 986.84 * (z1 ** 2) * (z2 ** 2) * reduced_mass_amu
        tunneling_factor = math.exp(-math.sqrt(eg_kev / energy_kev))
        
        return {
            "gamow_energy_Eg_keV": round(eg_kev, 4),
            "tunneling_probability": f"{tunneling_factor:.6e}"
        }
