import math

class FractalsChaosCore:
    @staticmethod
    def hausdorff_fractal_dimension(num_self_similar_pieces_n: int, scale_factor_s: float) -> dict:
        """D = ln(N) / ln(1/s)"""
        if num_self_similar_pieces_n <= 0 or scale_factor_s <= 0 or scale_factor_s >= 1.0: raise ValueError("Invalid parameters.")
        d_h = math.log(num_self_similar_pieces_n) / math.log(1.0 / scale_factor_s)
        return {"pieces_N": num_self_similar_pieces_n, "scale_s": scale_factor_s, "hausdorff_dimension": round(d_h, 6)}

    @staticmethod
    def henon_map_step(x: float, y: float, a: float = 1.4, b: float = 0.3) -> dict:
        """x_{n+1} = 1 - a*x_n^2 + y_n ; y_{n+1} = b*x_n"""
        xn1 = 1.0 - a * (x**2) + y
        yn1 = b * x
        return {"x_next": round(xn1, 6), "y_next": round(yn1, 6)}

    @staticmethod
    def box_counting_dimension_slope(box_sizes_r: list, count_n: list) -> dict:
        """D = - d(ln N) / d(ln r) via linear regression on log-log"""
        if len(box_sizes_r) != len(count_n) or len(box_sizes_r) < 2: raise ValueError("Mismatched data points.")
        log_inv_r = [math.log(1.0 / r) for r in box_sizes_r]
        log_n = [math.log(n) for n in count_n]
        mean_x = sum(log_inv_r) / len(log_inv_r)
        mean_y = sum(log_n) / len(log_n)
        slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_inv_r, log_n)) / sum((x - mean_x)**2 for x in log_inv_r)
        return {"box_counting_dimension": round(slope, 5)}
