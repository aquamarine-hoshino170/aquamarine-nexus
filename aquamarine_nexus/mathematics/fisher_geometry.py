class FisherInformationGeometryCore:
    """Information Manifolds & Fisher-Rao Information Metric"""

    @staticmethod
    def gaussian_fisher_metric(variance_sigma_sq: float) -> dict:
        """
        Computes the Fisher Information Metric tensor g_ij for normal distribution N(mu, sigma^2):
        g_mu_mu = 1 / sigma^2
        g_sigma_sigma = 2 / sigma^2
        Metric determinant det(g) = 2 / sigma^4
        """
        if variance_sigma_sq <= 0:
            raise ValueError("Variance sigma^2 must be strictly positive.")

        g_mu = 1.0 / variance_sigma_sq
        g_sigma = 2.0 / variance_sigma_sq
        det_g = 2.0 / (variance_sigma_sq ** 2)
        scalar_curvature_r = -1.0

        return {
            "variance_sigma_sq": variance_sigma_sq,
            "metric_tensor_diagonal": [round(g_mu, 6), round(g_sigma, 6)],
            "metric_determinant": round(det_g, 6),
            "information_scalar_curvature_R": scalar_curvature_r
        }

    @staticmethod
    def cramer_rao_lower_bound(fisher_info: float, sample_size_n: int) -> dict:
        """
        Calculates Cramer-Rao Lower Bound (CRLB) for unbiased estimators:
        Var(theta_hat) >= 1 / (N * I(theta))
        """
        if fisher_info <= 0 or sample_size_n <= 0:
            raise ValueError("Fisher information and sample size must be strictly positive.")

        crlb = 1.0 / (sample_size_n * fisher_info)
        return {
            "sample_size_N": sample_size_n,
            "fisher_info_I": fisher_info,
            "cramer_rao_lower_bound": f"{crlb:.6e}"
        }
