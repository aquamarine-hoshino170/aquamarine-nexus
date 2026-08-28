import math

class InteriorPointKKTCore:
    @staticmethod
    def logarithmic_barrier_objective(f_val: float, inequalities_g: list, mu_barrier: float) -> dict:
        """B(x, mu) = f(x) - mu * sum( ln( -g_i(x) ) ) for g_i(x) < 0"""
        if mu_barrier <= 0:
            raise ValueError("Barrier parameter mu must be strictly positive.")
        
        barrier_penalty = 0.0
        for g in inequalities_g:
            if g >= 0:
                raise ValueError("Point is outside strictly feasible interior (g_i >= 0).")
            barrier_penalty += math.log(-g)
        
        b_val = f_val - (mu_barrier * barrier_penalty)
        return {
            "objective_f": round(f_val, 6),
            "barrier_mu": mu_barrier,
            "barrier_objective_B": round(b_val, 6),
            "is_strictly_feasible": True
        }

    @staticmethod
    def kkt_complementary_slackness_residual(lagrange_multipliers_lambda: list, constraints_g: list) -> dict:
        """Residual = sum( |lambda_i * g_i| )"""
        if len(lagrange_multipliers_lambda) != len(constraints_g):
            raise ValueError("Multipliers and constraints dimension mismatch.")
        
        residuals = [abs(lam * g) for lam, g in zip(lagrange_multipliers_lambda, constraints_g)]
        total_slackness_error = sum(residuals)
        
        return {
            "total_complementary_slackness_error": round(total_slackness_error, 8),
            "is_kkt_slackness_satisfied": total_slackness_error < 1e-6
        }
