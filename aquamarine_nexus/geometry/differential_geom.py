import math

class DifferentialGeometry:
    """Differential Geometry & Tensor Manifold Core"""

    @staticmethod
    def gaussian_and_mean_curvature(e: float, f: float, g: float, l: float, m: float, n: float) -> dict:
        """
        Computes Gaussian Curvature (K) and Mean Curvature (H) given:
        First Fundamental Form: E, F, G
        Second Fundamental Form: L, M, N
        Formula:
          K = (LN - M^2) / (EG - F^2)
          H = (EN + GL - 2FM) / (2 * (EG - F^2))
        """
        denom = e * g - f**2
        if denom == 0:
            raise ZeroDivisionError("Degenerate first fundamental form (EG - F^2 = 0).")
        
        k_gauss = (l * n - m**2) / denom
        h_mean = (e * n + g * l - 2.0 * f * m) / (2.0 * denom)
        
        return {
            "gaussian_curvature_K": round(k_gauss, 6),
            "mean_curvature_H": round(h_mean, 6),
            "geometry_type": "Elliptic/Spherical" if k_gauss > 0 else ("Hyperbolic/Saddle" if k_gauss < 0 else "Flat/Parabolic")
        }

    @staticmethod
    def metric_tensor_2d(g11: float, g12: float, g22: float) -> dict:
        """
        2D Metric Tensor analysis: determinant and inverse components
        Metric Matrix g = [[g11, g12], [g12, g22]]
        """
        det_g = g11 * g22 - g12**2
        if det_g == 0:
            raise ZeroDivisionError("Singular metric tensor (det(g) = 0).")
        
        # Inverse metric components g^ij
        inv_g11 = g22 / det_g
        inv_g12 = -g12 / det_g
        inv_g22 = g11 / det_g
        
        return {
            "det_g": round(det_g, 6),
            "inv_g11": round(inv_g11, 6),
            "inv_g12": round(inv_g12, 6),
            "inv_g22": round(inv_g22, 6)
        }

    @staticmethod
    def geodesic_acceleration_1d(christoffel_gamma: float, velocity: float) -> dict:
        """
        Geodesic equation: d^2x/dt^2 + Gamma * (dx/dt)^2 = 0
        Returns the geodesic acceleration required to maintain a straight line in curved space.
        """
        acc = -christoffel_gamma * (velocity ** 2)
        return {
            "christoffel_gamma": christoffel_gamma,
            "velocity": velocity,
            "geodesic_acceleration": round(acc, 6)
        }

    @staticmethod
    def covariant_derivative_scalar_field(df_dx: float) -> dict:
        """For a scalar field, covariant derivative is simply the partial derivative: grad(phi)_i = d(phi)/dx^i"""
        return {"covariant_derivative": round(df_dx, 6)}
