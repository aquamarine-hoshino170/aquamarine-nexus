import math
from typing import List, Tuple, Dict, Any
from aquamarine_nexus.core.sovereign_tensor_engine import Tensor, Linear

class SovereignPPOCore:
    """
    Zero-Dependency High-Precision Reinforcement Learning Core.
    Implements Clipped Surrogate Policy Optimization (PPO-Clip) and Generalized Advantage Estimation (GAE).
    """

    @staticmethod
    def compute_generalized_advantage_estimation(
        rewards: List[float],
        values: List[float],
        next_value: float,
        dones: List[bool],
        gamma: float = 0.99,
        lam: float = 0.95
    ) -> Tuple[List[float], List[float]]:
        """
        GAE-Lambda advantage estimation: delta_t = r_t + gamma * V(s_{t+1}) * (1 - done) - V(s_t)
        A_t = delta_t + gamma * lambda * (1 - done) * A_{t+1}
        """
        T = len(rewards)
        advantages = [0.0] * T
        returns = [0.0] * T
        last_gae = 0.0

        for t in reversed(range(T)):
            next_val = values[t + 1] if t + 1 < T else next_value
            non_terminal = 1.0 - float(dones[t])
            delta = rewards[t] + gamma * next_val * non_terminal - values[t]
            advantages[t] = delta + gamma * lam * non_terminal * last_gae
            last_gae = advantages[t]
            returns[t] = advantages[t] + values[t]

        # Normalization
        mean_adv = sum(advantages) / float(T)
        var_adv = sum((a - mean_adv) ** 2 for a in advantages) / float(T)
        std_adv = math.sqrt(var_adv + 1e-8)
        norm_advantages = [(a - mean_adv) / std_adv for a in advantages]

        return norm_advantages, returns

    @staticmethod
    def compute_ppo_clipped_surrogate_loss(
        log_probs_new: List[float],
        log_probs_old: List[float],
        advantages: List[float],
        clip_ratio: float = 0.2
    ) -> Dict[str, float]:
        """
        L^{CLIP}(theta) = E [ min( r_t(theta) * A_t, clip(r_t(theta), 1 - eps, 1 + eps) * A_t ) ]
        """
        T = len(log_probs_new)
        losses = []
        approx_kl = 0.0
        clip_fractions = 0

        for i in range(T):
            log_p_new = log_probs_new[i]
            log_p_old = log_probs_old[i]
            adv = advantages[i]

            # Importance sampling ratio r(theta) = exp(log_p_new - log_p_old)
            ratio = math.exp(log_p_new - log_p_old)
            surr1 = ratio * adv
            surr2 = max(1.0 - clip_ratio, min(1.0 + clip_ratio, ratio)) * adv
            surrogate_loss = -min(surr1, surr2)
            losses.append(surrogate_loss)

            # Diagnostic metrics
            kl = log_p_old - log_p_new
            approx_kl += kl
            if abs(ratio - 1.0) > clip_ratio:
                clip_fractions += 1

        mean_loss = sum(losses) / float(T)
        return {
            "mean_ppo_loss": mean_loss,
            "approx_kl_divergence": approx_kl / float(T),
            "clip_fraction": clip_fractions / float(T)
        }
