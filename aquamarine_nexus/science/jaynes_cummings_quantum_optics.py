import math

class JaynesCummingsQuantumOpticsCore:
    @staticmethod
    def vacuum_rabi_splitting(atom_cavity_coupling_g_mhz: float, detuning_delta_mhz: float, photon_number_n: int = 0) -> dict:
        """Omega_R = 2 * sqrt( g^2 * (n + 1) + (Delta / 2)^2 )"""
        if atom_cavity_coupling_g_mhz < 0 or photon_number_n < 0:
            raise ValueError("Coupling constant and photon number must be non-negative.")
            
        generalized_rabi_freq = 2.0 * math.sqrt((atom_cavity_coupling_g_mhz ** 2) * (photon_number_n + 1) + ((detuning_delta_mhz / 2.0) ** 2))
        
        return {
            "coupling_strength_g_MHz": atom_cavity_coupling_g_mhz,
            "photon_number_n": photon_number_n,
            "cavity_detuning_Delta_MHz": detuning_delta_mhz,
            "vacuum_rabi_splitting_MHz": round(generalized_rabi_freq, 4),
            "strong_coupling_regime": atom_cavity_coupling_g_mhz > abs(detuning_delta_mhz)
        }
