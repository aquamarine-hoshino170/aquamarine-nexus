import math

class FluctuationTheoremsCore:
    K_BOLTZ = 1.380649e-23

    @staticmethod
    def jarzynski_free_energy_difference(work_trajectories_joules: list, temp_k: float) -> dict:
        """Delta_F = - k_B * T * ln( < exp(-W / k_B*T) > )"""
        if not work_trajectories_joules or temp_k <= 0:
            raise ValueError("Work trajectories cannot be empty and temperature must be positive.")
        beta = 1.0 / (FluctuationTheoremsCore.K_BOLTZ * temp_k)
        
        exp_terms = [math.exp(-beta * w) for w in work_trajectories_joules]
        mean_exp = sum(exp_terms) / len(exp_terms)
        delta_f = - (1.0 / beta) * math.log(mean_exp)
        
        mean_work = sum(work_trajectories_joules) / len(work_trajectories_joules)
        dissipated_work = mean_work - delta_f
        
        return {
            "temperature_K": temp_k,
            "trajectories_count": len(work_trajectories_joules),
            "free_energy_difference_J": f"{delta_f:.6e}",
            "mean_work_J": f"{mean_work:.6e}",
            "mean_dissipated_work_J": f"{dissipated_work:.6e}"
        }

    @staticmethod
    def crooks_probability_ratio(forward_prob: float, reverse_prob: float, temp_k: float) -> dict:
        """W - Delta_F = k_B * T * ln( P_F(W) / P_R(-W) )"""
        if forward_prob <= 0 or reverse_prob <= 0 or temp_k <= 0:
            raise ValueError("Probabilities and temperature must be strictly positive.")
        dissipated = FluctuationTheoremsCore.K_BOLTZ * temp_k * math.log(forward_prob / reverse_prob)
        return {
            "probability_ratio": round(forward_prob / reverse_prob, 6),
            "dissipated_work_J": f"{dissipated:.6e}"
        }
