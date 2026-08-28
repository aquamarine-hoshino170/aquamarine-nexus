import math

class GoldenRatioCore:
    """Pure Mathematics: Golden Ratio (Phi), Fibonacci Asymptotics & Logarithmic Spirals"""

    PHI = (1.0 + math.sqrt(5.0)) / 2.0
    INV_PHI = (math.sqrt(5.0) - 1.0) / 2.0  # 1 / phi = phi - 1

    @staticmethod
    def golden_ratio_properties() -> dict:
        """
        Fundamental algebraic properties of the Golden Ratio (phi):
        phi = (1 + sqrt(5)) / 2
        Identity: phi^2 = phi + 1, 1/phi = phi - 1
        """
        phi = GoldenRatioCore.PHI
        inv_phi = GoldenRatioCore.INV_PHI

        return {
            "phi_value": f"{phi:.15f}",
            "reciprocal_1_over_phi": f"{inv_phi:.15f}",
            "phi_squared": f"{phi ** 2:.15f}",
            "golden_angle_degrees": round(360.0 * (1.0 - 1.0 / phi), 6),
            "golden_angle_radians": round(2.0 * math.pi * (1.0 - 1.0 / phi), 6)
        }

    @staticmethod
    def fibonacci_convergence_ratio(n_terms: int = 20) -> dict:
        """
        Computes the ratio of consecutive Fibonacci numbers F(n+1)/F(n) 
        converging asymptotically to Phi as n -> infinity.
        """
        if n_terms < 2:
            raise ValueError("n_terms must be at least 2.")

        a, b = 1, 1
        ratios = []
        for _ in range(n_terms):
            ratios.append(round(b / a, 10))
            a, b = b, a + b

        final_ratio = ratios[-1]
        error = abs(final_ratio - GoldenRatioCore.PHI)

        return {
            "iterations": n_terms,
            "fibonacci_ratio_F_np1_over_Fn": final_ratio,
            "exact_phi": f"{GoldenRatioCore.PHI:.10f}",
            "absolute_error": f"{error:.6e}"
        }

    @staticmethod
    def golden_spiral_point(theta_rad: float, scale_a: float = 1.0) -> dict:
        """
        Logarithmic Golden Spiral polar/cartesian coordinates:
        r(theta) = a * phi^(2 * theta / pi)
        x = r * cos(theta), y = r * sin(theta)
        """
        if scale_a <= 0:
            raise ValueError("Scale factor 'a' must be positive.")

        growth_factor = (2.0 * theta_rad) / math.pi
        r = scale_a * (GoldenRatioCore.PHI ** growth_factor)
        x = r * math.cos(theta_rad)
        y = r * math.sin(theta_rad)

        return {
            "theta_radians": theta_rad,
            "radius_r": round(r, 6),
            "cartesian_x": round(x, 6),
            "cartesian_y": round(y, 6)
        }
