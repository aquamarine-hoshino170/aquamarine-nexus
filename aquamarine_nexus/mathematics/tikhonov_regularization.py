class TikhonovRegularizationCore:
    @staticmethod
    def tikhonov_filter_factors(singular_values_s: list, alpha_param: float) -> dict:
        """f_i = s_i^2 / (s_i^2 + alpha) for regularized inversion"""
        if alpha_param <= 0:
            raise ValueError("Regularization parameter alpha must be positive.")
        factors = []
        for s in singular_values_s:
            if s < 0:
                raise ValueError("Singular values must be non-negative.")
            f = (s ** 2) / ((s ** 2) + alpha_param)
            factors.append(round(f, 6))
        return {
            "alpha_param": alpha_param,
            "singular_values": singular_values_s,
            "tikhonov_filter_factors": factors
        }

    @staticmethod
    def morozov_discrepancy_residual(residual_norm: float, noise_level_delta: float, safety_tau: float = 1.1) -> dict:
        """Checks if ||A*x_alpha - y|| approx tau * delta"""
        target = safety_tau * noise_level_delta
        diff = residual_norm - target
        return {
            "residual_norm": round(residual_norm, 6),
            "target_noise_bound": round(target, 6),
            "discrepancy_difference": round(diff, 6),
            "is_morozov_satisfied": abs(diff) < 0.05 * target
        }
