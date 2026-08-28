import math

class FranzKeldyshElectroabsorptionCore:
    H_BAR = 1.054571817e-34
    E_CHARGE = 1.602176634e-19
    M_E = 9.10938356e-31

    @staticmethod
    def electro_optic_energy_parameter(electric_field_v_m: float, reduced_effective_mass_ratio: float = 0.067) -> dict:
        """hbar * Omega_F = ( (e * F * hbar)^2 / (2 * m_r) )^(1/3)"""
        if electric_field_v_m <= 0 or reduced_effective_mass_ratio <= 0:
            raise ValueError("Electric field and effective mass ratio must be strictly positive.")
            
        m_r = reduced_effective_mass_ratio * FranzKeldyshElectroabsorptionCore.M_E
        hbar = FranzKeldyshElectroabsorptionCore.H_BAR
        e = FranzKeldyshElectroabsorptionCore.E_CHARGE
        
        num = (e * electric_field_v_m * hbar) ** 2
        denom = 2.0 * m_r
        energy_j = (num / denom) ** (1.0 / 3.0)
        energy_ev = energy_j / e
        
        return {
            "electric_field_V_m": f"{electric_field_v_m:.6e}",
            "reduced_mass_kg": f"{m_r:.6e}",
            "electro_optic_energy_hbar_Omega_eV": round(energy_ev, 6),
            "tunneling_band_shift_meV": round(energy_ev * 1000.0, 4)
        }
