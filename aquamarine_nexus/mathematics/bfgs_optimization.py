class BFGSOptimizationCore:
    @staticmethod
    def bfgs_scalar_inverse_hessian_update(h_k: float, s_step: float, y_grad_diff: float) -> dict:
        """H_{k+1} = (1 - rho * s * y) * H_k * (1 - rho * y * s) + rho * s^2 where rho = 1 / (y * s)"""
        ys = y_grad_diff * s_step
        if ys <= 0:
            raise ValueError("Curvature condition y^T * s > 0 violated.")
        rho = 1.0 / ys
        term1 = (1.0 - rho * s_step * y_grad_diff) * h_k * (1.0 - rho * y_grad_diff * s_step)
        term2 = rho * (s_step ** 2)
        h_next = term1 + term2
        return {
            "previous_H_k": h_k,
            "step_s": s_step,
            "grad_diff_y": y_grad_diff,
            "rho": round(rho, 6),
            "updated_inverse_Hessian_H_next": round(h_next, 6)
        }
