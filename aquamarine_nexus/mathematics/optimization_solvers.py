import math

class OptimizationSolversCore:
    @staticmethod
    def newton_raphson_step(x_current: float, f_val: float, df_val: float) -> dict:
        """x_{n+1} = x_n - f(x_n) / f'(x_n)"""
        if df_val == 0: raise ValueError("Derivative cannot be zero.")
        x_next = x_current - (f_val / df_val)
        return {"x_current": x_current, "x_next": round(x_next, 8), "delta_step": round(abs(x_next - x_current), 8)}

    @staticmethod
    def gradient_descent_1d_step(x_current: float, gradient_val: float, learning_rate: float = 0.01) -> dict:
        """x_{t+1} = x_t - eta * grad(f)"""
        x_next = x_current - (learning_rate * gradient_val)
        return {"x_current": x_current, "x_next": round(x_next, 8), "learning_rate": learning_rate}

    @staticmethod
    def lagrange_multiplier_2d_linear_constraint(grad_f: list, grad_g: list) -> dict:
        """lambda = (grad_f . grad_g) / ||grad_g||^2"""
        if len(grad_f) != 2 or len(grad_g) != 2: raise ValueError("Requires 2D gradient vectors.")
        dot_fg = grad_f[0]*grad_g[0] + grad_f[1]*grad_g[1]
        norm_g_sq = grad_g[0]**2 + grad_g[1]**2
        if norm_g_sq == 0: raise ValueError("Constraint gradient cannot be zero.")
        lam = dot_fg / norm_g_sq
        return {"lagrange_multiplier_lambda": round(lam, 6)}
