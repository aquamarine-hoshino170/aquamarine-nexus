import math

class ChemicalThermodynamicsCore:
    R_GAS = 8.314462618

    @staticmethod
    def van_t_hoff_equilibrium_shift(k1_const: float, t1_k: float, t2_k: float, delta_h_j_mol: float) -> dict:
        """ln(K2 / K1) = - (Delta_H / R) * (1/T2 - 1/T1)"""
        if k1_const <= 0 or t1_k <= 0 or t2_k <= 0:
            raise ValueError("Equilibrium constant and temperatures must be strictly positive.")
            
        r = ChemicalThermodynamicsCore.R_GAS
        ln_ratio = - (delta_h_j_mol / r) * ((1.0 / t2_k) - (1.0 / t1_k))
        k2_const = k1_const * math.exp(ln_ratio)
        
        return {
            "initial_K1": f"{k1_const:.6e}",
            "initial_T1_K": t1_k,
            "final_T2_K": t2_k,
            "standard_enthalpy_Delta_H_J_mol": delta_h_j_mol,
            "shifted_equilibrium_K2": f"{k2_const:.6e}",
            "shift_direction": "Shift Right (Product favored)" if k2_const > k1_const else "Shift Left (Reactant favored)"
        }

    @staticmethod
    def henderson_hasselbalch_ph(pka: float, base_conc_molar: float, acid_conc_molar: float) -> dict:
        """pH = pKa + log10([A-] / [HA])"""
        if base_conc_molar <= 0 or acid_conc_molar <= 0:
            raise ValueError("Concentrations must be strictly positive.")
            
        ratio = base_conc_molar / acid_conc_molar
        ph = pka + math.log10(ratio)
        
        return {
            "pKa": pka,
            "conjugate_base_M": base_conc_molar,
            "weak_acid_M": acid_conc_molar,
            "buffer_pH": round(ph, 4)
        }
