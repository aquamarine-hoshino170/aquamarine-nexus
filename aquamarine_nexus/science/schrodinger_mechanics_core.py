import math

class SchrodingerMechanicsCore:
    H_BAR = 1.054571817e-34

    @staticmethod
    def infinite_square_well_eigenstate(n: int, box_length_m: float, particle_mass_kg: float) -> dict:
        """E_n = (n^2 * pi^2 * hbar^2) / (2 * m * L^2)"""
        if n <= 0 or box_length_m <= 0 or particle_mass_kg <= 0: raise ValueError("Parameters must be positive.")
        hbar = SchrodingerMechanicsCore.H_BAR
        energy = ((n ** 2) * (math.pi ** 2) * (hbar ** 2)) / (2.0 * particle_mass_kg * (box_length_m ** 2))
        return {"quantum_n": n, "box_length_m": f"{box_length_m:.6e}", "eigenvalue_energy_Joules": f"{energy:.6e}", "eigenvalue_energy_eV": f"{(energy / 1.602176634e-19):.6e}"}

    @staticmethod
    def probability_current_density_1d(wave_amplitude_psi0: float, momentum_p_kg_m_s: float, particle_mass_kg: float) -> dict:
        """j = (hbar * k / m) * |psi0|^2 = (p / m) * |psi0|^2"""
        if particle_mass_kg <= 0: raise ValueError("Mass must be positive.")
        velocity = momentum_p_kg_m_s / particle_mass_kg
        current_j = velocity * (wave_amplitude_psi0 ** 2)
        return {"wave_amplitude": wave_amplitude_psi0, "velocity_m_s": round(velocity, 4), "probability_current_j": round(current_j, 6)}
