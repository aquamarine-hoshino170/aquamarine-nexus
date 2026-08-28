class IntegralEquationsCore:
    @staticmethod
    def volterra_second_kind_trapezoid_step(x_grid: list, f_inhomogeneous: list, lambda_param: float, kernel_diag_val: float, prev_y_vals: list) -> dict:
        """y(x_n) = ( f(x_n) + lambda * h * sum_{j=0}^{n-1} w_j K(x_n, x_j) y(x_j) ) / (1 - lambda * h * 0.5 * K(x_n, x_n))"""
        n = len(prev_y_vals)
        if len(x_grid) <= n or len(f_inhomogeneous) <= n or n < 1:
            raise ValueError("Grid and previous values length mismatch.")
        h = x_grid[1] - x_grid[0]
        
        trap_sum = 0.5 * prev_y_vals[0]
        for j in range(1, n):
            trap_sum += prev_y_vals[j]
        
        integral_part = lambda_param * h * trap_sum
        denom = 1.0 - (lambda_param * h * 0.5 * kernel_diag_val)
        if abs(denom) < 1e-12:
            raise ValueError("Singular kernel step denominator.")
        
        next_y = (f_inhomogeneous[n] + integral_part) / denom
        return {
            "step_n": n,
            "x_n": x_grid[n],
            "computed_y_n": round(next_y, 8)
        }
