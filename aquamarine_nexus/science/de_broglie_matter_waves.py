import math

class DeBroglieMatterWavesCore:
    H_PLANCK = 6.62607015e-34
    C_LIGHT = 299792458.0

    @staticmethod
    def de_broglie_wavelength(particle_mass_kg: float, velocity_m_s: float) -> dict:
        """lambda = h / (m * v) (Non-relativistic & Relativistic)"""
        if particle_mass_kg <= 0 or velocity_m_s <= 0:
            raise ValueError("Mass and velocity must be strictly positive.")
        c = DeBroglieMatterWavesCore.C_LIGHT
        if velocity_m_s >= c:
            raise ValueError("Velocity cannot equal or exceed the speed of light.")
        
        gamma = 1.0 / math.sqrt(1.0 - ((velocity_m_s / c) ** 2))
        relativistic_p = gamma * particle_mass_kg * velocity_m_s
        lambda_de_broglie = DeBroglieMatterWavesCore.H_PLANCK / relativistic_p
        
        return {
            "particle_mass_kg": f"{particle_mass_kg:.6e}",
            "velocity_m_s": velocity_m_s,
            "lorentz_gamma": round(gamma, 6),
            "relativistic_momentum_kg_m_s": f"{relativistic_p:.6e}",
            "de_broglie_wavelength_m": f"{lambda_de_broglie:.6e}",
            "de_broglie_wavelength_Angstrom": round(lambda_de_broglie * 1e10, 6)
        }

    @staticmethod
    def phase_and_group_velocity_relation(group_velocity_m_s: float) -> dict:
        """v_phase = c^2 / v_group => v_phase * v_group = c^2"""
        c = DeBroglieMatterWavesCore.C_LIGHT
        if group_velocity_m_s <= 0 or group_velocity_m_s >= c:
            raise ValueError("Group velocity must be between 0 and c.")
        phase_v = (c ** 2) / group_velocity_m_s
        return {
            "group_velocity_vg_m_s": group_velocity_m_s,
            "phase_velocity_vp_m_s": f"{phase_v:.6e}",
            "product_vp_vg": f"{(phase_v * group_velocity_m_s):.6e}",
            "c_squared": f"{(c ** 2):.6e}",
            "is_superluminal_phase": phase_v > c
        }
