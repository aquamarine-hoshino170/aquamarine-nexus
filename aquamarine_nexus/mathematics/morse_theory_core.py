import math

class MorseTheoryCore:
    @staticmethod
    def hessian_morse_index_2x2(f_xx: float, f_xy: float, f_yy: float) -> dict:
        """Computes Morse Index (number of negative eigenvalues) and determinant of Hessian"""
        tr = f_xx + f_yy
        det = (f_xx * f_yy) - (f_xy ** 2)
        disc = tr**2 - 4.0 * det
        sqrt_disc = math.sqrt(disc) if disc >= 0 else 0.0
        
        lambda_1 = (tr + sqrt_disc) / 2.0
        lambda_2 = (tr - sqrt_disc) / 2.0
        
        neg_count = sum(1 for l in [lambda_1, lambda_2] if l < -1e-12)
        
        c_type = "Local Minimum" if neg_count == 0 and det > 0 else (
            "Local Maximum" if neg_count == 2 and det > 0 else (
                "Saddle Point" if det < 0 else "Degenerate Critical Point"
            )
        )
        
        return {
            "hessian_determinant": round(det, 6),
            "eigenvalue_1": round(lambda_1, 6),
            "eigenvalue_2": round(lambda_2, 6),
            "morse_index": neg_count,
            "critical_point_topology": c_type
        }
