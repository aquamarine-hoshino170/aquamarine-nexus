import math

class FractionalCalculusCore:
    @staticmethod
    def power_function_caputo_derivative(alpha_order: float, p_exponent: float, x_val: float) -> dict:
        """D^alpha (x^p) = ( Gamma(p + 1) / Gamma(p - alpha + 1) ) * x^(p - alpha)"""
        if x_val <= 0 or alpha_order < 0:
            raise ValueError("x must be positive and order non-negative.")
        if p_exponent < alpha_order:
            return {"order_alpha": alpha_order, "exponent_p": p_exponent, "x": x_val, "fractional_derivative": 0.0}
        
        g_num = math.gamma(p_exponent + 1.0)
        g_denom = math.gamma(p_exponent - alpha_order + 1.0)
        
        coeff = g_num / g_denom
        deriv_val = coeff * (x_val ** (p_exponent - alpha_order))
        
        return {
            "order_alpha": alpha_order,
            "exponent_p": p_exponent,
            "x": x_val,
            "gamma_prefactor": round(coeff, 6),
            "fractional_derivative": round(deriv_val, 6)
        }

    @staticmethod
    def mittag_leffler_2param(alpha: float, beta: float, z_val: float, terms: int = 40) -> dict:
        """E_{alpha, beta}(z) = sum_{k=0}^inf z^k / Gamma(alpha * k + beta)"""
        if alpha <= 0 or beta <= 0:
            raise ValueError("Alpha and beta must be positive.")
        total = 0.0
        for k in range(terms):
            denom = math.gamma(alpha * k + beta)
            term = (z_val ** k) / denom
            total += term
            if abs(term) < 1e-15:
                break
        return {
            "alpha": alpha,
            "beta": beta,
            "z": z_val,
            "mittag_leffler_value": round(total, 8)
        }
