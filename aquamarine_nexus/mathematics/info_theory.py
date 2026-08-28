import math

class InfoTheoryCore:
    """Classical Information Theory & Probability Manifolds"""

    @staticmethod
    def shannon_entropy(probabilities: list) -> dict:
        """Computes Shannon Entropy H(X) = -sum(p * log2(p)) in bits"""
        s = sum(probabilities)
        if abs(s - 1.0) > 1e-4:
            raise ValueError(f"Probabilities must sum to 1.0 (Sum is {s})")
        
        ent = 0.0
        for p in probabilities:
            if p > 0:
                ent -= p * math.log2(p)
        return {"shannon_entropy_bits": round(ent, 5), "max_possible_entropy": round(math.log2(len(probabilities)), 5)}

    @staticmethod
    def kl_divergence(p_dist: list, q_dist: list) -> dict:
        """Kullback-Leibler Divergence D_KL(P || Q) = sum(P(x) * log2(P(x)/Q(x)))"""
        if len(p_dist) != len(q_dist):
            raise ValueError("Distributions must have the same dimension.")
        
        kl = 0.0
        for p, q in zip(p_dist, q_dist):
            if p > 0:
                if q <= 0:
                    raise ValueError("Q(x) must be strictly positive where P(x) > 0.")
                kl += p * math.log2(p / q)
        return {"kl_divergence_bits": round(kl, 5)}
