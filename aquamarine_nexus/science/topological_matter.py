import math

class TopologicalMatterCore:
    """Topological Insulators, Berry Phase Curvature & Chern Invariants"""

    @staticmethod
    def two_band_berry_curvature(kx: float, ky: float, mass_gap: float = 1.0, v_fermi: float = 1.0) -> dict:
        """
        Computes Berry curvature Omega_z(k) for massive Dirac 2-band Hamiltonian:
        H(k) = v_F * (kx * sigma_x + ky * sigma_y) + (M - B*k^2) * sigma_z
        Omega_z(k) = (1/2) * (v_F^2 * M) / (v_F^2 * k^2 + M^2)^(3/2)
        """
        k_sq = kx**2 + ky**2
        d_norm_cube = ((v_fermi ** 2) * k_sq + (mass_gap ** 2)) ** (1.5)
        
        if d_norm_cube == 0:
            raise ValueError("Singularity at zero-gap band touch point.")

        berry_curvature_z = 0.5 * (v_fermi ** 2) * mass_gap / d_norm_cube

        return {
            "kx": kx,
            "ky": ky,
            "mass_gap": mass_gap,
            "berry_curvature_z": round(berry_curvature_z, 6),
            "topological_phase": "Chern Insulator" if mass_gap > 0 else "Trivial Insulator"
        }

    @staticmethod
    def quantum_hall_conductance(chern_number_c: int) -> dict:
        """
        TKNN Formula: Quantized Hall Conductance sigma_xy = C * (e^2 / h)
        """
        e_charge = 1.602176634e-19
        h_planck = 6.62607015e-34
        
        conductance_quantum = (e_charge ** 2) / h_planck
        sigma_xy = chern_number_c * conductance_quantum

        return {
            "chern_number_C": chern_number_c,
            "conductance_quantum_S": f"{conductance_quantum:.6e}",
            "hall_conductance_Siemens": f"{sigma_xy:.6e}",
            "hall_resistance_Ohms": f"{1.0 / sigma_xy:.4f}" if sigma_xy != 0 else "Infinite"
        }
