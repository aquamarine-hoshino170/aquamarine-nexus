import math

class AryabhataCompleteCore:
    @staticmethod
    def aryabhata_pi_approximation() -> dict:
        """Add 4 to 100, multiply by 8, add 62000 => 62832 / 20000 = 3.1416"""
        numerator = (100 + 4) * 8 + 62000
        denominator = 20000
        pi_approx = numerator / denominator
        return {
            "rule": "caturadhikam satamastagunam",
            "circumference": numerator,
            "diameter": denominator,
            "pi_aryabhata": pi_approx,
            "error_vs_true_pi": f"{abs(pi_approx - math.pi):.6e}"
        }

    @staticmethod
    def sum_of_squares_and_cubes(n: int) -> dict:
        """Sum of squares: n(n+1)(2n+1)/6, Sum of cubes: (n(n+1)/2)^2"""
        if n <= 0: raise ValueError("n must be a positive integer.")
        sum_n = (n * (n + 1)) // 2
        sum_sq = (n * (n + 1) * (2 * n + 1)) // 6
        sum_cube = sum_n ** 2
        return {
            "n": n,
            "sum_integers": sum_n,
            "sum_of_squares": sum_sq,
            "sum_of_cubes": sum_cube
        }

    @staticmethod
    def kuttaka_linear_diophantine(a: int, b: int, c: int) -> dict:
        """Kuttaka (Pulverizer) algorithm for ax + by = c (Extended Euclidean basis)"""
        def extended_gcd(a_val, b_val):
            if b_val == 0: return a_val, 1, 0
            gcd, x1, y1 = extended_gcd(b_val, a_val % b_val)
            x = y1
            y = x1 - (a_val // b_val) * y1
            return gcd, x, y

        gcd_val, x0, y0 = extended_gcd(abs(a), abs(b))
        if c % gcd_val != 0:
            return {"solvable": False, "reason": "gcd(a, b) does not divide c"}
        
        factor = c // gcd_val
        x_sol = x0 * factor * (1 if a >= 0 else -1)
        y_sol = y0 * factor * (1 if b >= 0 else -1)
        return {
            "gcd": gcd_val,
            "particular_solution_x": x_sol,
            "particular_solution_y": y_sol,
            "verification": (a * x_sol + b * y_sol == c)
        }

    @staticmethod
    def aryabhata_jya_sine(angle_deg: float, radius_r: float = 3438.0) -> dict:
        """Jya = R * sin(theta), Kotijya = R * cos(theta), Utkramajya = R * (1 - cos(theta))"""
        theta_rad = math.radians(angle_deg)
        jya = radius_r * math.sin(theta_rad)
        kotijya = radius_r * math.cos(theta_rad)
        utkramajya = radius_r * (1.0 - math.cos(theta_rad))
        return {
            "angle_deg": angle_deg,
            "base_radius_R": radius_r,
            "jya_sine": round(jya, 4),
            "kotijya_cosine": round(kotijya, 4),
            "utkramajya_versine": round(utkramajya, 4)
        }

    @staticmethod
    def shanku_shadow_height(gnomon_height: float, gnomon_shadow: float, object_shadow: float) -> dict:
        """H = (gnomon_height * object_shadow) / gnomon_shadow (Similar Triangles Law)"""
        if gnomon_shadow <= 0: raise ValueError("Shadow length must be positive.")
        height = (gnomon_height * object_shadow) / gnomon_shadow
        return {
            "gnomon_height": gnomon_height,
            "gnomon_shadow": gnomon_shadow,
            "object_shadow": object_shadow,
            "calculated_object_height": round(height, 4)
        }
