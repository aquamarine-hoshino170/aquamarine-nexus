import math

class BiochemicalKineticsCore:
    R_GAS = 8.314462618

    @staticmethod
    def michaelis_menten_velocity(v_max: float, substrate_conc: float, k_m: float) -> dict:
        """v = (V_max * [S]) / (K_m + [S])"""
        if v_max <= 0 or substrate_conc < 0 or k_m <= 0:
            raise ValueError("Parameters must be positive.")
        v = (v_max * substrate_conc) / (k_m + substrate_conc)
        return {
            "v_max": v_max,
            "substrate_S": substrate_conc,
            "k_m": k_m,
            "reaction_velocity": round(v, 6),
            "fraction_max_velocity": round(v / v_max, 4)
        }

    @staticmethod
    def hill_equation_cooperativity(ligand_conc: float, k_d: float, hill_n: float) -> dict:
        """theta = [L]^n / (K_d + [L]^n)"""
        if ligand_conc < 0 or k_d <= 0 or hill_n <= 0:
            raise ValueError("Invalid Hill parameters.")
        l_n = ligand_conc ** hill_n
        theta = l_n / (k_d + l_n)
        coop = "Positively Cooperative" if hill_n > 1 else ("Negatively Cooperative" if hill_n < 1 else "Non-cooperative")
        return {
            "fractional_occupancy_theta": round(theta, 6),
            "hill_coefficient_n": hill_n,
            "cooperativity_type": coop
        }

    @staticmethod
    def arrhenius_rate_constant(pre_exponential_a: float, activation_energy_j_mol: float, temp_k: float) -> dict:
        """k = A * exp(-E_a / (R * T))"""
        if pre_exponential_a <= 0 or temp_k <= 0 or activation_energy_j_mol < 0:
            raise ValueError("Invalid Arrhenius parameters.")
        k = pre_exponential_a * math.exp(-activation_energy_j_mol / (BiochemicalKineticsCore.R_GAS * temp_k))
        return {
            "pre_exponential_A": f"{pre_exponential_a:.4e}",
            "temperature_K": temp_k,
            "rate_constant_k": f"{k:.6e}"
        }
