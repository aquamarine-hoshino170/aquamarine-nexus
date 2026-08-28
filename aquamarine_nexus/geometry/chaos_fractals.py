import math

class ChaosFractalCore:
    """Non-linear Dynamics, Lyapunov Chaos & Fractal Metrics"""

    @staticmethod
    def mandelbrot_escape(c_real: float, c_imag: float, max_iter: int = 100) -> dict:
        """Computes escape iteration count for z_{n+1} = z_n^2 + c in complex plane"""
        z = 0j
        c = complex(c_real, c_imag)
        for i in range(max_iter):
            z = z * z + c
            if abs(z) > 2.0:
                return {"c": f"{c_real} + {c_imag}i", "escaped": True, "iterations": i, "modulus": round(abs(z), 4)}
        return {"c": f"{c_real} + {c_imag}i", "escaped": False, "iterations": max_iter, "modulus": round(abs(z), 4)}

    @staticmethod
    def logistic_map_lyapunov(r: float, x0: float = 0.5, steps: int = 500) -> dict:
        """
        Computes Lyapunov Exponent lambda for Logistic Map: x_{n+1} = r * x * (1 - x)
        lambda > 0 denotes deterministic chaos.
        """
        x = x0
        # Warm-up iterations to reach attractor
        for _ in range(100):
            x = r * x * (1.0 - x)
        
        lyap_sum = 0.0
        for _ in range(steps):
            x = r * x * (1.0 - x)
            deriv = abs(r * (1.0 - 2.0 * x))
            if deriv > 0:
                lyap_sum += math.log(deriv)
        
        lam = lyap_sum / steps
        return {"parameter_r": r, "lyapunov_exponent": round(lam, 5), "is_chaotic": lam > 0}
