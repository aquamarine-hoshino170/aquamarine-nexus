import math

class QuantumExchangeChemistryCore:
    E_CHARGE = 1.602176634e-19
    EPSILON_0 = 8.8541878128e-12

    @staticmethod
    def slater_dirac_exchange_energy_density(electron_density_m3: float) -> dict:
        """epsilon_x = - (3/4) * (3 / pi)^(1/3) * (e^2 / (4 * pi * eps0)) * rho^(4/3) (LDA Exchange)"""
        if electron_density_m3 <= 0:
            raise ValueError("Electron density must be strictly positive.")
            
        e = QuantumExchangeChemistryCore.E_CHARGE
        eps0 = QuantumExchangeChemistryCore.EPSILON_0
        
        c_x = (3.0 / 4.0) * ((3.0 / math.pi) ** (1.0 / 3.0)) * ((e ** 2) / (4.0 * math.pi * eps0))
        e_x_density = - c_x * (electron_density_m3 ** (4.0 / 3.0))
        
        return {
            "electron_density_m3": f"{electron_density_m3:.6e}",
            "lda_exchange_coefficient_SI": f"{c_x:.6e}",
            "exchange_energy_density_J_m3": f"{e_x_density:.6e}",
            "exchange_energy_density_eV_m3": f"{(e_x_density / e):.6e}"
        }
