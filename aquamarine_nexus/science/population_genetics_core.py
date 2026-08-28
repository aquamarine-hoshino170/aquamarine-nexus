import math

class PopulationGeneticsCore:
    @staticmethod
    def hardy_weinberg_equilibrium(p_freq: float) -> dict:
        """p^2 + 2pq + q^2 = 1, where p + q = 1"""
        if not (0.0 <= p_freq <= 1.0):
            raise ValueError("Allele frequency p must be between 0 and 1.")
        
        q_freq = 1.0 - p_freq
        p2 = p_freq ** 2
        two_pq = 2.0 * p_freq * q_freq
        q2 = q_freq ** 2
        
        return {
            "allele_frequency_p": round(p_freq, 6),
            "allele_frequency_q": round(q_freq, 6),
            "homozygous_dominant_p2": round(p2, 6),
            "heterozygous_2pq": round(two_pq, 6),
            "homozygous_recessive_q2": round(q2, 6),
            "equilibrium_sum": round(p2 + two_pq + q2, 6)
        }

    @staticmethod
    def selection_allele_delta(p_freq: float, fitness_w_aa: float, fitness_w_aa_het: float, fitness_w_aa_rec: float) -> dict:
        """Delta_p = (p * (p*w_11 + q*w_12 - w_bar)) / w_bar"""
        if not (0.0 <= p_freq <= 1.0):
            raise ValueError("Allele frequency p must be between 0 and 1.")
        if fitness_w_aa < 0 or fitness_w_aa_het < 0 or fitness_w_aa_rec < 0:
            raise ValueError("Fitness values must be non-negative.")
            
        q_freq = 1.0 - p_freq
        w_bar = (p_freq**2 * fitness_w_aa) + (2.0 * p_freq * q_freq * fitness_w_aa_het) + (q_freq**2 * fitness_w_aa_rec)
        if w_bar == 0:
            raise ValueError("Mean population fitness cannot be zero.")
            
        p_prime = (p_freq**2 * fitness_w_aa + p_freq * q_freq * fitness_w_aa_het) / w_bar
        delta_p = p_prime - p_freq
        
        return {
            "mean_fitness_w_bar": round(w_bar, 6),
            "next_generation_p": round(p_prime, 6),
            "delta_p": round(delta_p, 6)
        }
