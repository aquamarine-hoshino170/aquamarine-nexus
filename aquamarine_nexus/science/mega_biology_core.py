import math

class MegaBiologyCore:
    R_GAS = 8.314462618

    @staticmethod
    def shannon_diversity_index(species_counts: list) -> dict:
        """H = - sum( p_i * ln(p_i) ), Evenness E = H / ln(S)"""
        total = sum(species_counts)
        if total <= 0 or any(c < 0 for c in species_counts):
            raise ValueError("Species counts must be non-negative and total > 0.")
        
        proportions = [c / total for c in species_counts if c > 0]
        s_richness = len(proportions)
        h_index = - sum(p * math.log(p) for p in proportions)
        evenness = h_index / math.log(s_richness) if s_richness > 1 else 1.0
        
        return {
            "species_richness_S": s_richness,
            "shannon_diversity_H": round(h_index, 6),
            "pielou_evenness_E": round(evenness, 6)
        }

    @staticmethod
    def oxygen_hemoglobin_adair_binding(p_o2_mmhg: float, a1: float = 0.024, a2: float = 0.0007, a3: float = 0.000006, a4: float = 0.000002) -> dict:
        """Adair 4-step oxygen saturation equation for Hemoglobin tetramer"""
        if p_o2_mmhg < 0: raise ValueError("Partial pressure must be non-negative.")
        p = p_o2_mmhg
        num = (a1 * p) + (2.0 * a2 * (p**2)) + (3.0 * a3 * (p**3)) + (4.0 * a4 * (p**4))
        denom = 4.0 * (1.0 + (a1 * p) + (a2 * (p**2)) + (a3 * (p**3)) + (a4 * (p**4)))
        saturation = num / denom if denom > 0 else 0.0
        return {
            "pO2_mmHg": p_o2_mmhg,
            "fractional_saturation_Y": round(saturation, 6),
            "percentage_saturation": round(saturation * 100.0, 2)
        }

    @staticmethod
    def b_cell_clonal_selection_affinity(antigen_dose: float, base_affinity_ka: float, somatic_mutation_rate: float, rounds: int) -> dict:
        """K_affinity(n) = K_0 * (1 + mu * dose)^n"""
        if rounds < 0 or antigen_dose < 0 or base_affinity_ka <= 0:
            raise ValueError("Invalid parameters.")
        evolved_affinity = base_affinity_ka * ((1.0 + somatic_mutation_rate * antigen_dose) ** rounds)
        return {
            "initial_affinity_Ka": f"{base_affinity_ka:.4e}",
            "affinity_maturation_rounds": rounds,
            "matured_affinity_Ka": f"{evolved_affinity:.6e}"
        }
