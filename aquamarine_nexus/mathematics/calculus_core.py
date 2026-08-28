class DiscreteCalculusCore:
    """Discrete Gradient, Difference & Numerical Trapezoidal Integration Engine"""

    @staticmethod
    def discrete_trapezoid_integral(y_values: list, dx: float = 1.0) -> dict:
        """
        Computes composite trapezoidal integration over discrete array y:
        Integral = dx * (0.5*y_0 + sum(y_1..y_{n-2}) + 0.5*y_{n-1})
        """
        if len(y_values) < 2:
            raise ValueError("At least 2 points required for trapezoidal integration.")

        total = 0.5 * (y_values[0] + y_values[-1]) + sum(y_values[1:-1])
        integral_val = total * dx

        return {
            "points_count": len(y_values),
            "step_dx": dx,
            "trapezoidal_integral": round(integral_val, 6)
        }

    @staticmethod
    def discrete_gradient_1d(y_values: list, dx: float = 1.0) -> dict:
        """
        Computes numerical central differences for interior points, 
        and forward/backward differences at the boundaries.
        """
        n = len(y_values)
        if n < 2:
            raise ValueError("At least 2 points required for gradient calculation.")

        grad = [0.0] * n
        # Forward difference at start
        grad[0] = (y_values[1] - y_values[0]) / dx
        # Central difference in interior
        for i in range(1, n - 1):
            grad[i] = (y_values[i + 1] - y_values[i - 1]) / (2.0 * dx)
        # Backward difference at end
        grad[-1] = (y_values[-1] - y_values[-2]) / dx

        return {
            "points_count": n,
            "gradient_array": [round(g, 6) for g in grad]
        }
