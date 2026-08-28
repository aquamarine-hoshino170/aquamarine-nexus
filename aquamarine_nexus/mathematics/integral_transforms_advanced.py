import math

class AdvancedTransformsCore:
    @staticmethod
    def discrete_mellin_transform_sample(y_values: list, x_grid: list, s_param: float) -> dict:
        """M{f}(s) = int_0^inf x^(s-1) f(x) dx approx sum( x_i^(s-1) * y_i * Delta_x )"""
        if len(y_values) != len(x_grid) or len(x_grid) < 2:
            raise ValueError("Mismatched data arrays.")
        if any(x <= 0 for x in x_grid):
            raise ValueError("Grid coordinates must be strictly positive for Mellin transform.")
        
        total = 0.0
        for i in range(len(x_grid) - 1):
            dx = x_grid[i + 1] - x_grid[i]
            x_mid = 0.5 * (x_grid[i] + x_grid[i + 1])
            y_mid = 0.5 * (y_values[i] + y_values[i + 1])
            total += (x_mid ** (s_param - 1.0)) * y_mid * dx
        
        return {
            "s_parameter": s_param,
            "mellin_transform_approx": round(total, 6)
        }

    @staticmethod
    def hilbert_transform_kernel_step(signal: list, center_idx: int) -> dict:
        """H(x)[n] = (1 / pi) * sum_{k != n} signal[k] / (n - k)"""
        n = len(signal)
        if center_idx < 0 or center_idx >= n:
            raise ValueError("Invalid index.")
        
        total = 0.0
        for k in range(n):
            if k != center_idx:
                total += signal[k] / (center_idx - k)
        
        hilbert_val = total / math.pi
        analytic_envelope = math.sqrt(signal[center_idx]**2 + hilbert_val**2)
        
        return {
            "signal_value": signal[center_idx],
            "hilbert_transformed": round(hilbert_val, 6),
            "analytic_signal_envelope": round(analytic_envelope, 6)
        }
