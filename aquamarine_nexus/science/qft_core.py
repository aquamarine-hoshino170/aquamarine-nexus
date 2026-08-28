import math

class QFTDynamicsCore:
    """Relativistic Quantum Fields & Spinor Currents (Klein-Gordon / Dirac)"""

    H_PLANCK = 6.62607015e-34
    C_LIGHT = 299792458.0

    @staticmethod
    def compton_wavelength(rest_mass_kg: float) -> dict:
        """
        Calculates Compton Wavelength lambda_c = h / (m * c) 
        and Reduced Compton Wavelength lambda_bar = hbar / (m * c)
        """
        if rest_mass_kg <= 0:
            raise ValueError("Rest mass must be positive.")

        h = QFTDynamicsCore.H_PLANCK
        c = QFTDynamicsCore.C_LIGHT
        
        lambda_c = h / (rest_mass_kg * c)
        lambda_bar = lambda_c / (2.0 * math.pi)

        return {
            "rest_mass_kg": rest_mass_kg,
            "compton_wavelength_m": f"{lambda_c:.6e}",
            "reduced_compton_m": f"{lambda_bar:.6e}"
        }

    @staticmethod
    def dirac_probability_density(psi_0_real: float, psi_0_imag: float,
                                  psi_1_real: float, psi_1_imag: float,
                                  psi_2_real: float, psi_2_imag: float,
                                  psi_3_real: float, psi_3_imag: float) -> dict:
        """
        Computes the conserved probability density J^0 = psi_dagger * psi for a 4-component Dirac spinor.
        """
        c0 = complex(psi_0_real, psi_0_imag)
        c1 = complex(psi_1_real, psi_1_imag)
        c2 = complex(psi_2_real, psi_2_imag)
        c3 = complex(psi_3_real, psi_3_imag)

        density = abs(c0)**2 + abs(c1)**2 + abs(c2)**2 + abs(c3)**2
        return {
            "probability_density_J0": round(density, 6),
            "is_normalized": abs(density - 1.0) < 1e-4
        }
