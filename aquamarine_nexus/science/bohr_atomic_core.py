import math

class BohrAtomicCore:
    H_BAR = 1.054571817e-34
    M_E = 9.10938356e-31
    E_CHARGE = 1.602176634e-19
    EPSILON_0 = 8.8541878128e-12

    @staticmethod
    def bohr_orbit_parameters(n_principal: int, z_atomic_number: int = 1) -> dict:
        """r_n = (4 * pi * eps0 * hbar^2 * n^2) / (m_e * Z * e^2), E_n = - (13.6057 * Z^2 / n^2) eV"""
        if n_principal <= 0 or z_atomic_number <= 0:
            raise ValueError("Principal quantum number n and Z must be positive integers.")
        
        hbar = BohrAtomicCore.H_BAR
        m = BohrAtomicCore.M_E
        e = BohrAtomicCore.E_CHARGE
        eps0 = BohrAtomicCore.EPSILON_0
        
        # Bohr radius calculation
        a0 = (4.0 * math.pi * eps0 * (hbar ** 2)) / (m * (e ** 2))
        radius_n = (a0 * (n_principal ** 2)) / z_atomic_number
        energy_ev = -13.605693 * (z_atomic_number ** 2) / (n_principal ** 2)
        
        return {
            "principal_quantum_n": n_principal,
            "atomic_number_Z": z_atomic_number,
            "bohr_radius_a0_m": f"{a0:.6e}",
            "orbital_radius_rn_m": f"{radius_n:.6e}",
            "energy_level_En_eV": round(energy_ev, 6),
            "energy_level_En_Joules": f"{(energy_ev * e):.6e}"
        }

    @staticmethod
    def bohr_magneton_moment() -> dict:
        """mu_B = (e * hbar) / (2 * m_e)"""
        mu_b = (BohrAtomicCore.E_CHARGE * BohrAtomicCore.H_BAR) / (2.0 * BohrAtomicCore.M_E)
        return {
            "bohr_magneton_J_T": f"{mu_b:.6e}",
            "bohr_magneton_eV_T": f"{(mu_b / BohrAtomicCore.E_CHARGE):.6e}"
        }
