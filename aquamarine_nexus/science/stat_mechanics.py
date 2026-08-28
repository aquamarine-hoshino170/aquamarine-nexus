import math

class QuantumStatMechanics:
    """Quantum & Classical Statistical Ensembles"""

    @staticmethod
    def fermi_dirac_distribution(energy_ev: float, fermi_energy_ev: float, temp_k: float) -> dict:
        """
        Fermi-Dirac statistics: f(E) = 1 / (exp((E - E_F) / (k_B * T)) + 1)
        """
        if temp_k <= 0:
            occ = 1.0 if energy_ev < fermi_energy_ev else (0.5 if energy_ev == fermi_energy_ev else 0.0)
            return {"temperature_K": 0.0, "occupation_probability": occ}

        kb_ev = 8.617333262145e-5 # eV / K
        arg = (energy_ev - fermi_energy_ev) / (kb_ev * temp_k)
        if arg > 500:
            occ = 0.0
        elif arg < -500:
            occ = 1.0
        else:
            occ = 1.0 / (math.exp(arg) + 1.0)
        return {"energy_eV": energy_ev, "fermi_level_eV": fermi_energy_ev, "occupation_probability": round(occ, 6)}

    @staticmethod
    def bose_einstein_distribution(energy_ev: float, chemical_potential_ev: float, temp_k: float) -> dict:
        """
        Bose-Einstein statistics: n(E) = 1 / (exp((E - mu) / (k_B * T)) - 1)
        Requires E > mu
        """
        if energy_ev <= chemical_potential_ev:
            raise ValueError("Energy E must be strictly greater than chemical potential mu for Bosons.")
        if temp_k <= 0:
            raise ValueError("Temperature must be positive.")

        kb_ev = 8.617333262145e-5
        arg = (energy_ev - chemical_potential_ev) / (kb_ev * temp_k)
        if arg > 500:
            occ = 0.0
        else:
            occ = 1.0 / (math.exp(arg) - 1.0)
        return {"energy_eV": energy_ev, "chem_potential_eV": chemical_potential_ev, "mean_occupation_number": round(occ, 6)}
