import math

class BoseStatisticsCore:
    K_BOLTZ = 1.380649e-23
    H_PLANCK = 6.62607015e-34

    @staticmethod
    def bose_einstein_distribution(energy_joules: float, chemical_potential_mu: float, temp_k: float) -> dict:
        """f(E) = 1 / ( exp( (E - mu) / (k_B * T) ) - 1 )"""
        if temp_k <= 0 or energy_joules < chemical_potential_mu: raise ValueError("Invalid physical values.")
        diff = energy_joules - chemical_potential_mu
        x = diff / (BoseStatisticsCore.K_BOLTZ * temp_k)
        if x > 700: occupancy = 0.0
        elif x <= 0: raise ValueError("Singularity: E must be strictly greater than chemical potential.")
        else: occupancy = 1.0 / (math.exp(x) - 1.0)
        return {"energy_J": f"{energy_joules:.6e}", "chemical_potential_J": f"{chemical_potential_mu:.6e}", "temperature_K": temp_k, "bose_occupancy_number": round(occupancy, 6)}

    @staticmethod
    def planck_blackbody_bose_radiance(freq_hz: float, temp_k: float) -> dict:
        """I(nu, T) = (2 * h * nu^3 / c^2) * (1 / (exp(h*nu / k_B*T) - 1))"""
        c = 299792458.0
        h = BoseStatisticsCore.H_PLANCK
        kb = BoseStatisticsCore.K_BOLTZ
        if freq_hz <= 0 or temp_k <= 0: raise ValueError("Frequency and temperature must be positive.")
        x = (h * freq_hz) / (kb * temp_k)
        denom = math.exp(x) - 1.0 if x < 700 else float('inf')
        spectral_radiance = ((2.0 * h * (freq_hz ** 3)) / (c ** 2)) * (1.0 / denom)
        return {"frequency_Hz": f"{freq_hz:.6e}", "temperature_K": temp_k, "spectral_radiance_W_m2_sr_Hz": f"{spectral_radiance:.6e}"}
