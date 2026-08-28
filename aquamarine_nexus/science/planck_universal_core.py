import math

class PlanckUniversalCore:
    H_PLANCK = 6.62607015e-34
    H_BAR = 1.054571817e-34
    G_CONST = 6.67430e-11
    C_LIGHT = 299792458.0
    K_BOLTZ = 1.380649e-23

    @staticmethod
    def planck_energy_density_spectrum(freq_hz: float, temp_k: float) -> dict:
        """u(nu, T) = (8 * pi * h * nu^3 / c^3) * (1 / (exp(h*nu / k_B*T) - 1))"""
        if freq_hz <= 0 or temp_k <= 0:
            raise ValueError("Frequency and temperature must be strictly positive.")
        h = PlanckUniversalCore.H_PLANCK
        c = PlanckUniversalCore.C_LIGHT
        kb = PlanckUniversalCore.K_BOLTZ
        
        x = (h * freq_hz) / (kb * temp_k)
        denom = math.exp(x) - 1.0 if x < 700 else float('inf')
        density = ((8.0 * math.pi * h * (freq_hz ** 3)) / (c ** 3)) * (1.0 / denom)
        return {
            "frequency_Hz": f"{freq_hz:.6e}",
            "temperature_K": temp_k,
            "spectral_energy_density_J_m3_Hz": f"{density:.6e}"
        }

    @staticmethod
    def planck_base_units() -> dict:
        """Computes fundamental Planck length, time, mass, temperature, and energy"""
        hbar = PlanckUniversalCore.H_BAR
        g = PlanckUniversalCore.G_CONST
        c = PlanckUniversalCore.C_LIGHT
        kb = PlanckUniversalCore.K_BOLTZ

        l_p = math.sqrt((hbar * g) / (c ** 3))
        t_p = math.sqrt((hbar * g) / (c ** 5))
        m_p = math.sqrt((hbar * c) / g)
        t_temp_p = math.sqrt((hbar * (c ** 5)) / (g * (kb ** 2)))
        e_p = m_p * (c ** 2)

        return {
            "planck_length_l_p_meters": f"{l_p:.6e}",
            "planck_time_t_p_seconds": f"{t_p:.6e}",
            "planck_mass_m_p_kg": f"{m_p:.6e}",
            "planck_temperature_T_p_Kelvin": f"{t_temp_p:.6e}",
            "planck_energy_E_p_Joules": f"{e_p:.6e}",
            "planck_energy_E_p_GeV": f"{(e_p / 1.602176634e-10):.6e}"
        }
