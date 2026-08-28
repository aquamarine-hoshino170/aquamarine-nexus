import math

class DigitalEpigeneticsCore:
    """Algorithmic Epigenetics, CpG Methylation Dynamics & Epigenetic Entropy"""

    @staticmethod
    def cpg_methylation_entropy(methylation_fractions: list) -> dict:
        """
        Calculates local Epigenetic Entropy H_epi over a set of CpG site methylation probabilities p_i:
        H_epi = -(1 / N) * sum [ p_i * log2(p_i) + (1 - p_i) * log2(1 - p_i) ]
        """
        if not methylation_fractions:
            raise ValueError("CpG methylation list cannot be empty.")

        n = len(methylation_fractions)
        total_entropy = 0.0

        for p in methylation_fractions:
            if p < 0.0 or p > 1.0:
                raise ValueError(f"Methylation level {p} must be within [0, 1].")
            
            h_i = 0.0
            if 0.0 < p < 1.0:
                h_i = - (p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))
            total_entropy += h_i

        mean_entropy = total_entropy / n
        return {
            "total_cpg_sites": n,
            "mean_epigenetic_entropy_bits": round(mean_entropy, 5),
            "epigenetic_stability_score": round(1.0 - mean_entropy, 5)
        }

    @staticmethod
    def demethylation_decay_step(current_methylation: float, demethylation_rate_k: float, dt: float) -> dict:
        """
        Simulates active/passive demethylation kinetics via differential decay:
        dp/dt = -k * p
        """
        if current_methylation < 0.0 or current_methylation > 1.0:
            raise ValueError("Methylation must be in [0, 1].")

        new_methylation = current_methylation * math.exp(-demethylation_rate_k * dt)
        return {
            "initial_methylation": current_methylation,
            "updated_methylation": round(new_methylation, 6),
            "delta_loss": round(current_methylation - new_methylation, 6)
        }
