import math

class PlasmaMHDCore:
    """Plasma Physics, Debye Shielding & Magnetohydrodynamics (MHD)"""

    EPS_0 = 8.8541878128e-12
    MU_0 = 4.0 * math.pi * 1e-7
    K_BOLTZ = 1.380649e-23
    Q_ELEM = 1.602176634e-19

    @staticmethod
    def debye_length(electron_density_m3: float, electron_temp_k: float) -> dict:
        """
        Computes Debye Screening Length lambda_D = sqrt( (eps_0 * k_B * T_e) / (n_e * e^2) )
        """
        if electron_density_m3 <= 0 or electron_temp_k <= 0:
            raise ValueError("Electron density and temperature must be strictly positive.")

        eps_0 = PlasmaMHDCore.EPS_0
        kb = PlasmaMHDCore.K_BOLTZ
        e = PlasmaMHDCore.Q_ELEM

        lambda_d = math.sqrt((eps_0 * kb * electron_temp_k) / (electron_density_m3 * (e ** 2)))
        return {
            "electron_density_m3": electron_density_m3,
            "electron_temp_K": electron_temp_k,
            "debye_length_m": f"{lambda_d:.6e}"
        }

    @staticmethod
    def alfven_velocity(b_field_tesla: float, plasma_mass_density_kg_m3: float) -> dict:
        """
        Computes Alfvén wave phase velocity: v_A = B / sqrt(mu_0 * rho)
        """
        if plasma_mass_density_kg_m3 <= 0:
            raise ValueError("Plasma mass density must be positive.")

        mu_0 = PlasmaMHDCore.MU_0
        v_alfven = b_field_tesla / math.sqrt(mu_0 * plasma_mass_density_kg_m3)

        return {
            "magnetic_field_T": b_field_tesla,
            "mass_density_kg_m3": plasma_mass_density_kg_m3,
            "alfven_velocity_m_s": round(v_alfven, 4)
        }
