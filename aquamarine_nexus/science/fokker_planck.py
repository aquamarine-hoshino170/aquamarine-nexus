import math

class FokkerPlanckDynamicsCore:
    """Stochastic Fokker-Planck Drift-Diffusion & Ornstein-Uhlenbeck Processes"""

    @staticmethod
    def ornstein_uhlenbeck_moments(x0: float, theta_reversion: float, mu_mean: float, sigma_volatility: float, time_t: float) -> dict:
        """
        Exact conditional distribution moments for Ornstein-Uhlenbeck SDE:
        E[X_t] = mu + (x0 - mu) * exp(-theta * t)
        Var(X_t) = (sigma^2 / (2 * theta)) * (1 - exp(-2 * theta * t))
        """
        if theta_reversion <= 0 or sigma_volatility < 0 or time_t < 0:
            raise ValueError("theta, sigma, and time_t must be positive.")

        exp_decay = math.exp(-theta_reversion * time_t)
        exp_decay_2 = math.exp(-2.0 * theta_reversion * time_t)

        expected_x = mu_mean + (x0 - mu_mean) * exp_decay
        variance_x = (sigma_volatility ** 2) / (2.0 * theta_reversion) * (1.0 - exp_decay_2)
        stationary_variance = (sigma_volatility ** 2) / (2.0 * theta_reversion)

        return {
            "initial_state_x0": x0,
            "time_t": time_t,
            "conditional_mean": round(expected_x, 6),
            "conditional_variance": round(variance_x, 6),
            "stationary_variance": round(stationary_variance, 6),
            "standard_deviation": round(math.sqrt(variance_x), 6)
        }
