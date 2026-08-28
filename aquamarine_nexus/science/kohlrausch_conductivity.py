import math

class KohlrauschConductivityCore:
    @staticmethod
    def molar_conductivity_limiting(cation_limiting_cond: float, anion_limiting_cond: float, cation_stoich: int, anion_stoich: int) -> dict:
        """Lambda_m^0 = nu_+ * lambda_+^0 + nu_- * lambda_-^0"""
        if cation_limiting_cond <= 0 or anion_limiting_cond <= 0 or cation_stoich <= 0 or anion_stoich <= 0:
            raise ValueError("Conductance and stoichiometric coefficients must be positive.")
            
        lambda_0 = (cation_stoich * cation_limiting_cond) + (anion_stoich * anion_limiting_cond)
        return {
            "limiting_molar_conductivity_S_cm2_mol": round(lambda_0, 4)
        }

    @staticmethod
    def kohlrausch_concentration_dependence(lambda_0: float, kohlrausch_k: float, concentration_molar: float) -> dict:
        """Lambda_m = Lambda_m^0 - K * sqrt(c)"""
        if concentration_molar < 0 or lambda_0 <= 0 or kohlrausch_k < 0:
            raise ValueError("Concentration and parameters must be valid.")
            
        lambda_m = lambda_0 - (kohlrausch_k * math.sqrt(concentration_molar))
        return {
            "concentration_M": concentration_molar,
            "limiting_molar_conductivity": lambda_0,
            "molar_conductivity_S_cm2_mol": round(max(0.0, lambda_m), 4)
        }
