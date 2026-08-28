import math
import cmath

class HyperbolicTopologyCore:
    """Poincaré Half-Plane & Hyperbolic Manifold Core"""

    @staticmethod
    def poincare_half_plane_distance(z1_real: float, z1_imag: float, z2_real: float, z2_imag: float) -> dict:
        """
        Hyperbolic distance d(z1, z2) in Upper Half-Plane H^2:
        cosh(d) = 1 + |z1 - z2|^2 / (2 * Im(z1) * Im(z2))
        """
        if z1_imag <= 0 or z2_imag <= 0:
            raise ValueError("Points must have strictly positive imaginary components (Im(z) > 0).")
        
        diff_sq = (z1_real - z2_real)**2 + (z1_imag - z2_imag)**2
        delta = 1.0 + diff_sq / (2.0 * z1_imag * z2_imag)
        dist = math.acosh(delta)
        return {
            "z1": f"{z1_real} + {z1_imag}i",
            "z2": f"{z2_real} + {z2_imag}i",
            "hyperbolic_distance": round(dist, 6)
        }

    @staticmethod
    def mobius_sl2r_transform(a: float, b: float, c: float, d: float, z_real: float, z_imag: float) -> dict:
        """
        Möbius isometry f(z) = (az + b) / (cz + d) in SL(2, R) where ad - bc = 1
        """
        det = a * d - b * c
        if abs(det - 1.0) > 1e-4:
            raise ValueError(f"Matrix must belong to SL(2, R) with det=1. Current det is {det}")
        
        z = complex(z_real, z_imag)
        w = (a * z + b) / (c * z + d)
        return {"w_real": round(w.real, 6), "w_imag": round(w.imag, 6)}
