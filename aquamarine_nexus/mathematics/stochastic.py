import math

class StochasticCalculusCore:
    """Stochastic Differential Equations & Brownian Motion Dynamics"""

    @staticmethod
    def geometric_brownian_step(s_current: float, mu_drift: float, sigma_volatility: float, z_normal: float, dt: float) -> dict:
        """
        Analytic step for Geometric Brownian Motion (Itô Calculus):
        S(t + dt) = S(t) * exp((mu - 0.5 * sigma^2)*dt + sigma * sqrt(dt) * Z)
        """
        if s_current <= 0 or dt <= 0:
            raise ValueError("Current value S and dt must be strictly positive.")
        
        drift = (mu_drift - 0.5 * (sigma_volatility ** 2)) * dt
        diffusion = sigma_volatility * math.sqrt(dt) * z_normal
        s_next = s_current * math.exp(drift + diffusion)

        return {
            "s_current": s_current,
            "s_next": round(s_next, 6),
            "drift_component": round(drift, 6),
            "diffusion_component": round(diffusion, 6)
        }

    @staticmethod
    def wiener_variance(t_time: float) -> dict:
        """Wiener process property: Var(W_t) = t, Mean(W_t) = 0"""
        if t_time < 0:
            raise ValueError("Time t must be non-negative.")
        return {"time_t": t_time, "expected_mean": 0.0, "variance": t_time, "std_dev": round(math.sqrt(t_time), 6)}
