import math

class GeneralizedEntropyCore:
    @staticmethod
    def renyi_entropy(probabilities: list, alpha_order: float) -> dict:
        """H_alpha = (1 / (1 - alpha)) * ln( sum p_i^alpha )"""
        if alpha_order <= 0 or alpha_order == 1.0:
            raise ValueError("Alpha must be positive and != 1.")
        if not probabilities or abs(sum(probabilities) - 1.0) > 1e-4:
            raise ValueError("Probabilities must sum to 1.0.")
        
        sum_p_alpha = sum((p ** alpha_order) for p in probabilities if p > 0)
        h_alpha = (1.0 / (1.0 - alpha_order)) * math.log(sum_p_alpha)
        return {
            "alpha_order": alpha_order,
            "renyi_entropy_nats": round(h_alpha, 6),
            "renyi_entropy_bits": round(h_alpha / math.log(2.0), 6)
        }

    @staticmethod
    def tsallis_entropy(probabilities: list, q_index: float) -> dict:
        """S_q = (1 / (q - 1)) * (1 - sum p_i^q)"""
        if q_index == 1.0:
            raise ValueError("q=1 corresponds to standard Shannon entropy limit.")
        if not probabilities or abs(sum(probabilities) - 1.0) > 1e-4:
            raise ValueError("Probabilities must sum to 1.0.")
        
        sum_p_q = sum((p ** q_index) for p in probabilities if p > 0)
        s_q = (1.0 / (q_index - 1.0)) * (1.0 - sum_p_q)
        return {
            "q_index": q_index,
            "tsallis_entropy": round(s_q, 6)
        }
