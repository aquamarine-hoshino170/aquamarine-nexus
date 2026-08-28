import math

class StatisticalThermodynamicsCore:
    K_BOLTZ = 1.380649e-23
    N_AVOGADRO = 6.02214076e23

    @staticmethod
    def sackur_tetrode_entropy(volume_m3: float, temperature_k: float, particle_number_n: float, atomic_mass_kg: float) -> dict:
        """S = N * k_B * [ ln( (V/N) * ( (4*pi*m*k_B*T) / (3*h^2) )^(3/2) ) + 5/2 ]"""
        h = 6.62607015e-34
        kb = StatisticalThermodynamicsCore.K_BOLTZ
        if volume_m3 <= 0 or temperature_k <= 0 or particle_number_n <= 0: raise ValueError("Invalid inputs.")
        lambda_th = math.sqrt((h ** 2) / (2.0 * math.pi * atomic_mass_kg * kb * temperature_k))
        val = (volume_m3 / particle_number_n) / (lambda_th ** 3)
        entropy = particle_number_n * kb * (math.log(val) + 2.5)
        return {"particle_number_N": particle_number_n, "temperature_K": temperature_k, "thermal_de_broglie_m": f"{lambda_th:.6e}", "entropy_J_K": f"{entropy:.6e}"}

    @staticmethod
    def maxwell_boltzmann_speeds(temperature_k: float, molar_mass_kg_mol: float) -> dict:
        """v_mp = sqrt(2RT/M), v_avg = sqrt(8RT/pi*M), v_rms = sqrt(3RT/M)"""
        r_gas = StatisticalThermodynamicsCore.K_BOLTZ * StatisticalThermodynamicsCore.N_AVOGADRO
        if temperature_k <= 0 or molar_mass_kg_mol <= 0: raise ValueError("Invalid inputs.")
        v_mp = math.sqrt((2.0 * r_gas * temperature_k) / molar_mass_kg_mol)
        v_avg = math.sqrt((8.0 * r_gas * temperature_k) / (math.pi * molar_mass_kg_mol))
        v_rms = math.sqrt((3.0 * r_gas * temperature_k) / molar_mass_kg_mol)
        return {"most_probable_speed_m_s": round(v_mp, 2), "average_speed_m_s": round(v_avg, 2), "rms_speed_m_s": round(v_rms, 2)}
