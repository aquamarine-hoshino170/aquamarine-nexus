class NelderMeadStepCore:
    @staticmethod
    def simplex_reflection_2d(worst_point: list, centroid: list, alpha_reflect: float = 1.0) -> dict:
        """x_r = centroid + alpha * (centroid - worst_point)"""
        if len(worst_point) != 2 or len(centroid) != 2:
            raise ValueError("2D coordinates required.")
        x_r = [
            centroid[0] + alpha_reflect * (centroid[0] - worst_point[0]),
            centroid[1] + alpha_reflect * (centroid[1] - worst_point[1])
        ]
        return {
            "worst_point": worst_point,
            "centroid": centroid,
            "alpha": alpha_reflect,
            "reflected_point": [round(x_r[0], 6), round(x_r[1], 6)]
        }

    @staticmethod
    def simplex_expansion_contraction_step(centroid: list, probe_point: list, gamma_factor: float) -> dict:
        """x_new = centroid + gamma * (probe_point - centroid)"""
        if len(probe_point) != 2 or len(centroid) != 2:
            raise ValueError("2D coordinates required.")
        x_new = [
            centroid[0] + gamma_factor * (probe_point[0] - centroid[0]),
            centroid[1] + gamma_factor * (probe_point[1] - centroid[1])
        ]
        return {
            "factor_gamma": gamma_factor,
            "scaled_point": [round(x_new[0], 6), round(x_new[1], 6)]
        }
