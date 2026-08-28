class BanachFixedPointCore:
    @staticmethod
    def banach_error_estimate(initial_diff_d_x0_x1: float, contraction_constant_q: float, iteration_n: int) -> dict:
        """d(x_n, x*) <= (q^n / (1 - q)) * d(x_0, x_1)"""
        if not (0.0 <= contraction_constant_q < 1.0) or iteration_n < 0 or initial_diff_d_x0_x1 < 0:
            raise ValueError("Contraction constant q must be in [0, 1) and n >= 0.")
            
        bound = ((contraction_constant_q ** iteration_n) / (1.0 - contraction_constant_q)) * initial_diff_d_x0_x1
        return {
            "lipschitz_constant_q": contraction_constant_q,
            "step_count_n": iteration_n,
            "initial_step_size": initial_diff_d_x0_x1,
            "guaranteed_error_bound": f"{bound:.8e}",
            "convergence_assured": True
        }
