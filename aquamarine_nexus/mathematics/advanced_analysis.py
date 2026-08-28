import math
import cmath

class AdvancedAnalysis:
    """High-Dimensional Manifold & Complex Analysis Engine"""
    @staticmethod
    def metric_tensor_christoffel_1d(g_func, x: float, h: float = 1e-5) -> float:
        """Christoffel Symbol Calculation for 1D Metric Tensor: Γ = 1/2 * g^-1 * (dg/dx)"""
        g_val = g_func(x)
        if g_val == 0:
            raise ZeroDivisionError("Singularity in metric tensor.")
        dg_dx = (g_func(x + h) - g_func(x - h)) / (2.0 * h)
        return (0.5 / g_val) * dg_dx

    @staticmethod
    def contour_residue_pole_simple(func, z0: complex, r: float = 1e-4, points: int = 128) -> complex:
        """Numerical Residue via Cauchy's Integral Formula"""
        integral = 0j
        for k in range(points):
            theta = 2.0 * math.pi * k / points
            z = z0 + r * cmath.exp(1j * theta)
            dz = 1j * r * cmath.exp(1j * theta) * (2.0 * math.pi / points)
            integral += func(z) * dz
        return integral / (2j * math.pi)
