import math

class DiracQuantumCore:
    H_BAR = 1.054571817e-34
    C_LIGHT = 299792458.0
    E_CHARGE = 1.602176634e-19
    K_BOLTZ = 1.380649e-23

    @staticmethod
    def dirac_relativistic_energy_momentum(rest_mass_kg: float, momentum_kg_m_s: float) -> dict:
        """E = sqrt( (p * c)^2 + (m * c^2)^2 )"""
        if rest_mass_kg < 0 or momentum_kg_m_s < 0:
            raise ValueError("Mass and momentum must be non-negative.")
        c = DiracQuantumCore.C_LIGHT
        e_sq = (momentum_kg_m_s * c) ** 2 + (rest_mass_kg * (c ** 2)) ** 2
        energy_j = math.sqrt(e_sq)
        energy_ev = energy_j / DiracQuantumCore.E_CHARGE
        return {
            "positive_energy_state_eV": round(energy_ev, 4),
            "negative_energy_state_antimatter_eV": round(-energy_ev, 4),
            "rest_mass_energy_eV": round((rest_mass_kg * (c ** 2)) / DiracQuantumCore.E_CHARGE, 4)
        }

    @staticmethod
    def fermi_dirac_distribution(energy_ev: float, fermi_energy_ef_ev: float, temp_k: float) -> dict:
        """f(E) = 1 / ( exp( (E - E_F) / (k_B * T) ) + 1 )"""
        if temp_k <= 0:
            raise ValueError("Temperature must be strictly positive.")
        kb_ev = DiracQuantumCore.K_BOLTZ / DiracQuantumCore.E_CHARGE
        diff = energy_ev - fermi_energy_ef_ev
        x = diff / (kb_ev * temp_k)
        
        if x > 700:
            occupancy = 0.0
        elif x < -700:
            occupancy = 1.0
        else:
            occupancy = 1.0 / (math.exp(x) + 1.0)
            
        return {
            "energy_eV": energy_ev,
            "fermi_level_Ef_eV": fermi_energy_ef_ev,
            "temperature_K": temp_k,
            "fermi_occupancy_probability": round(occupancy, 8)
        }

    @staticmethod
    def dirac_monopole_charge_quantization(monopole_n: int = 1) -> dict:
        """g = n * hbar * c / (2 * e)"""
        if monopole_n <= 0:
            raise ValueError("Integer quantum number n must be >= 1.")
        hbar = DiracQuantumCore.H_BAR
        c = DiracQuantumCore.C_LIGHT
        e = DiracQuantumCore.E_CHARGE
        g_charge = (monopole_n * hbar * c) / (2.0 * e)
        return {
            "quantum_n": monopole_n,
            "elementary_charge_e_C": f"{e:.6e}",
            "magnetic_monopole_charge_g_SI": f"{g_charge:.6e}",
            "charge_product_eg_over_hbar_c": (e * g_charge) / (hbar * c)
        }
