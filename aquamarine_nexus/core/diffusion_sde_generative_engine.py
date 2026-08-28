import math
import random
from typing import List, Tuple, Dict, Any

class ContinuousDiffusionCore:
    """
    Zero-Dependency High-Precision Diffusion & Continuous-Time SDE Engine.
    Implements Variance Preserving (VP) SDE, cosine/linear beta noise schedules,
    and deterministic DDIM/Stochastic Euler-Maruyama reverse sampling.
    """

    def __init__(self, timesteps: int = 100, beta_start: float = 1e-4, beta_end: float = 0.02, schedule: str = "linear"):
        self.timesteps = timesteps
        self.betas: List[float] = []
        self.alphas: List[float] = []
        self.alphas_cumprod: List[float] = []

        if schedule == "linear":
            # Linear Beta Schedule
            step_delta = (beta_end - beta_start) / float(timesteps - 1)
            self.betas = [beta_start + i * step_delta for i in range(timesteps)]
        elif schedule == "cosine":
            # Cosine Beta Schedule
            s = 0.008
            for t in range(timesteps):
                t1 = (t / float(timesteps) + s) / (1.0 + s) * (math.pi / 2.0)
                t2 = ((t + 1) / float(timesteps) + s) / (1.0 + s) * (math.pi / 2.0)
                alpha_bar1 = math.cos(t1) ** 2
                alpha_bar2 = math.cos(t2) ** 2
                b = min(1.0 - alpha_bar2 / alpha_bar1, 0.999)
                self.betas.append(b)

        # Precalculate forward multipliers
        prod = 1.0
        for b in self.betas:
            a = 1.0 - b
            self.alphas.append(a)
            prod *= a
            self.alphas_cumprod.append(prod)

    def q_sample(self, x_0: List[float], t: int, noise: List[float]) -> List[float]:
        """
        Forward process: q(x_t | x_0) = sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * eps
        """
        alpha_bar = self.alphas_cumprod[t]
        sqrt_alpha_bar = math.sqrt(alpha_bar)
        sqrt_one_minus_alpha_bar = math.sqrt(1.0 - alpha_bar)

        return [
            sqrt_alpha_bar * x + sqrt_one_minus_alpha_bar * eps
            for x, eps in zip(x_0, noise)
        ]

    def p_sample_step_ddim(
        self, 
        x_t: List[float], 
        t: int, 
        predicted_noise: List[float], 
        eta: float = 0.0
    ) -> List[float]:
        """
        Deterministic/Stochastic DDIM Reverse Step:
        x_{t-1} = sqrt(alpha_bar_{t-1}) * x_0_pred + dir_xt + random_noise
        """
        alpha_bar_t = self.alphas_cumprod[t]
        alpha_bar_prev = self.alphas_cumprod[t - 1] if t > 0 else 1.0

        # Estimate clean signal x_0
        sqrt_ab_t = math.sqrt(alpha_bar_t)
        sqrt_one_minus_ab_t = math.sqrt(1.0 - alpha_bar_t)
        
        x_0_pred = [
            (xt - sqrt_one_minus_ab_t * eps) / sqrt_ab_t
            for xt, eps in zip(x_t, predicted_noise)
        ]

        # Compute variance sigma
        sigma_t = (
            eta * math.sqrt((1.0 - alpha_bar_prev) / (1.0 - alpha_bar_t)) *
            math.sqrt(1.0 - alpha_bar_t / alpha_bar_prev)
            if t > 0 else 0.0
        )

        # Direction pointing to x_t
        dir_xt_coeff = math.sqrt(max(0.0, 1.0 - alpha_bar_prev - sigma_t ** 2))
        sqrt_ab_prev = math.sqrt(alpha_bar_prev)

        x_prev = []
        for i in range(len(x_t)):
            val = sqrt_ab_prev * x_0_pred[i] + dir_xt_coeff * predicted_noise[i]
            if sigma_t > 0.0:
                val += sigma_t * random.gauss(0.0, 1.0)
            x_prev.append(val)

        return x_prev

    def compute_score_sde_drift(self, x: List[float], t_continuous: float, score_estimate: List[float]) -> List[float]:
        """
        VP-SDE Reverse Drift: f_rev(x, t) = -0.5 * beta(t) * [x + 2 * Score(x, t)]
        """
        beta_t = self.betas[0] + t_continuous * (self.betas[-1] - self.betas[0])
        drift = [-0.5 * beta_t * (xi + 2.0 * s) for xi, s in zip(x, score_estimate)]
        return drift
