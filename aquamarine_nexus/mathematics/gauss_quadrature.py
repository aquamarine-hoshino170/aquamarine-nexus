import math

class GaussQuadratureCore:
    @staticmethod
    def legendre_2point_quadrature(f_x0: float, f_x1: float, a_bound: float, b_bound: float) -> dict:
        """Integral over [a, b] approx ((b - a)/2) * [ f(x1) + f(x2) ], x = (b-a)/2 * (+- 1/sqrt(3)) + (a+b)/2"""
        if b_bound <= a_bound:
            raise ValueError("b must be strictly greater than a.")
        mid = 0.5 * (b_bound + a_bound)
        half_len = 0.5 * (b_bound - a_bound)
        node_offset = half_len / math.sqrt(3.0)
        
        integral_val = half_len * (f_x0 + f_x1)
        return {
            "interval": [a_bound, b_bound],
            "evaluation_nodes": [round(mid - node_offset, 6), round(mid + node_offset, 6)],
            "weights": [round(half_len, 6), round(half_len, 6)],
            "integral_approximation": round(integral_val, 8)
        }

    @staticmethod
    def legendre_3point_quadrature(f_neg: float, f_zero: float, f_pos: float, a_bound: float, b_bound: float) -> dict:
        """Integral over [a, b] approx ((b - a)/2) * [ (5/9)*f(x1) + (8/9)*f(x2) + (5/9)*f(x3) ]"""
        if b_bound <= a_bound:
            raise ValueError("b must be strictly greater than a.")
        half_len = 0.5 * (b_bound - a_bound)
        mid = 0.5 * (b_bound + a_bound)
        node_offset = half_len * math.sqrt(3.0 / 5.0)
        
        integral_val = half_len * ((5.0 / 9.0) * f_neg + (8.0 / 9.0) * f_zero + (5.0 / 9.0) * f_pos)
        return {
            "interval": [a_bound, b_bound],
            "evaluation_nodes": [round(mid - node_offset, 6), round(mid, 6), round(mid + node_offset, 6)],
            "weights": [round(half_len * 5/9, 6), round(half_len * 8/9, 6), round(half_len * 5/9, 6)],
            "integral_approximation": round(integral_val, 8)
        }
