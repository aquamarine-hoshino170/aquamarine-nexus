import math

class RobustLossFunctionsCore:
    @staticmethod
    def huber_loss_eval(residual: float, delta: float = 1.345) -> dict:
        """L_delta(r) = 0.5 * r^2 if |r| <= delta else delta * (|r| - 0.5 * delta)"""
        if delta <= 0:
            raise ValueError("Delta parameter must be strictly positive.")
        abs_r = abs(residual)
        if abs_r <= delta:
            loss = 0.5 * (residual ** 2)
            grad = residual
        else:
            loss = delta * (abs_r - 0.5 * delta)
            grad = delta if residual > 0 else -delta
        
        return {
            "residual_r": residual,
            "huber_loss": round(loss, 6),
            "huber_gradient": round(grad, 6),
            "regime": "Quadratic L2" if abs_r <= delta else "Linear L1"
        }

    @staticmethod
    def softplus_activation_and_derivative(x_val: float) -> dict:
        """f(x) = ln(1 + exp(x)), f'(x) = 1 / (1 + exp(-x))"""
        val = math.log1p(math.exp(x_val)) if x_val < 30 else x_val
        grad = 1.0 / (1.0 + math.exp(-x_val)) if x_val >= -700 else 0.0
        return {
            "x": x_val,
            "softplus_value": round(val, 8),
            "softplus_gradient_sigmoid": round(grad, 8)
        }
