class KalmanFilterCore:
    @staticmethod
    def kalman_filter_scalar_update(prior_estimate: float, prior_variance: float, measurement: float, measurement_noise_r: float) -> dict:
        """
        K = P_prior / (P_prior + R)
        x_post = x_prior + K * (z - x_prior)
        P_post = (1 - K) * P_prior
        """
        if prior_variance <= 0 or measurement_noise_r <= 0:
            raise ValueError("Variances must be strictly positive.")
        
        kalman_gain_k = prior_variance / (prior_variance + measurement_noise_r)
        posterior_estimate = prior_estimate + kalman_gain_k * (measurement - prior_estimate)
        posterior_variance = (1.0 - kalman_gain_k) * prior_variance
        
        return {
            "kalman_gain_K": round(kalman_gain_k, 6),
            "posterior_state": round(posterior_estimate, 6),
            "posterior_variance": round(posterior_variance, 6),
            "residual_innovation": round(measurement - prior_estimate, 6)
        }
