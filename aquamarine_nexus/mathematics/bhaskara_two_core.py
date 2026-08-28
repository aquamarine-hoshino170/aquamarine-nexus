import math

class BhaskaraTwoCore:
    @staticmethod
    def chakravala_pell_solver(n_non_square: int) -> dict:
        """Solves x^2 - N * y^2 = 1 via Cyclic Chakravala Method"""
        if n_non_square <= 0 or math.isqrt(n_non_square)**2 == n_non_square:
            raise ValueError("N must be a positive non-square integer.")
        
        a = math.isqrt(n_non_square)
        b = 1
        k = a * a - n_non_square
        
        while k != 1:
            # Find m such that (a + b*m) is divisible by |k| and |m^2 - N| is minimized
            abs_k = abs(k)
            best_m = None
            min_diff = float('inf')
            base_m = 1
            for m_cand in range(1, abs_k + math.isqrt(n_non_square) + 2):
                if (a + b * m_cand) % abs_k == 0:
                    diff = abs(m_cand * m_cand - n_non_square)
                    if diff < min_diff:
                        min_diff = diff
                        best_m = m_cand
            
            if best_m is None:
                best_m = (abs_k - (a % abs_k))
                
            m = best_m
            new_a = (a * m + n_non_square * b) // abs_k
            new_b = (a + b * m) // abs_k
            new_k = (m * m - n_non_square) // k
            
            a, b, k = new_a, new_b, new_k
            
            if k == -1:
                # Brahmagupta composition (Samasa) to reach k = 1
                a, b = a * a + n_non_square * b * b, 2 * a * b
                k = 1
                break
            elif k == 2:
                a, b = a * a - 1, a * b
                k = 1
                break
            elif k == -2:
                a, b = a * a + 1, a * b
                k = 1
                break
                
        return {
            "N": n_non_square,
            "fundamental_solution_x": a,
            "fundamental_solution_y": b,
            "verification": (a * a - n_non_square * b * b == 1)
        }

    @staticmethod
    def tatkalika_sine_derivative(x_deg: float, delta_deg: float) -> dict:
        """Bhaskara II Tatkalika Gati: sin(x + delta) - sin(x) approx delta * cos(x)"""
        x_rad = math.radians(x_deg)
        delta_rad = math.radians(delta_deg)
        
        exact_diff = math.sin(x_rad + delta_rad) - math.sin(x_rad)
        differential_approx = delta_rad * math.cos(x_rad)
        
        return {
            "x_deg": x_deg,
            "delta_deg": delta_deg,
            "exact_difference": round(exact_diff, 8),
            "bhaskara_differential_approx": round(differential_approx, 8),
            "residual_error": f"{abs(exact_diff - differential_approx):.6e}"
        }
