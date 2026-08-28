import math

class BogoliubovSuperfluidityCore:
    H_BAR = 1.054571817e-34

    @staticmethod
    def bogoliubov_quasiparticle_energy(wavenumber_k_m_inv: float, particle_mass_kg: float, sound_speed_c_s_m_s: float) -> dict:
        """E(k) = sqrt( (hbar^2 * k^2 / (2 * m))^2 + (hbar * k * c_s)^2 )"""
        if wavenumber_k_m_inv <= 0 or particle_mass_kg <= 0 or sound_speed_c_s_m_s <= 0:
            raise ValueError("Wavenumber, mass, and sound speed must be strictly positive.")
            
        hbar = BogoliubovSuperfluidityCore.H_BAR
        kinetic_term = ((hbar * wavenumber_k_m_inv) ** 2) / (2.0 * particle_mass_kg)
        phonon_term = hbar * wavenumber_k_m_inv * sound_speed_c_s_m_s
        
        e_k_joules = math.sqrt((kinetic_term ** 2) + (phonon_term ** 2))
        e_k_ev = e_k_joules / 1.602176634e-19
        
        # Healing length xi = hbar / (sqrt(2) * m * c_s)
        xi_healing = hbar / (math.sqrt(2.0) * particle_mass_kg * sound_speed_c_s_m_s)
        
        return {
            "wavenumber_k_m_inv": f"{wavenumber_k_m_inv:.6e}",
            "healing_length_xi_nm": round(xi_healing * 1e9, 4),
            "quasiparticle_energy_Joules": f"{e_k_joules:.6e}",
            "quasiparticle_energy_ueV": round(e_k_ev * 1e6, 6),
            "dispersion_regime": "Acoustic / Phonon (Linear)" if wavenumber_k_m_inv * xi_healing < 1.0 else "Free Particle (Quadratic)"
        }
