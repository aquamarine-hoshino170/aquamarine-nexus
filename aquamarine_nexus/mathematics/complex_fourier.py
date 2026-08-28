import math
import cmath

class ComplexFourierCore:
    """Complex Analysis, Conformal Geometry & Discrete Fourier Core"""

    @staticmethod
    def stereographic_projection(x: float, y: float) -> dict:
        """
        Projects point (x, y) on the complex plane onto the unit Riemann Sphere (X, Y, Z):
        X = 2x / (1 + x^2 + y^2)
        Y = 2y / (1 + x^2 + y^2)
        Z = (x^2 + y^2 - 1) / (1 + x^2 + y^2)
        """
        denom = 1.0 + x**2 + y**2
        X = (2.0 * x) / denom
        Y = (2.0 * y) / denom
        Z = (x**2 + y**2 - 1.0) / denom
        return {"Riemann_X": round(X, 6), "Riemann_Y": round(Y, 6), "Riemann_Z": round(Z, 6)}

    @staticmethod
    def joukowsky_transform(real: float, imag: float) -> dict:
        """
        Joukowsky Aerodynamic Conformal Mapping: w = z + 1/z
        Transforms circles into airfoil aerodynamic profiles.
        """
        z = complex(real, imag)
        if z == 0:
            raise ZeroDivisionError("Singularity at z = 0.")
        w = z + 1.0 / z
        return {"w_real": round(w.real, 6), "w_imag": round(w.imag, 6), "modulus": round(abs(w), 6)}

    @staticmethod
    def dft_1d(signal: list) -> list:
        """
        Pure-Python Discrete Fourier Transform:
        X_k = sum_{n=0}^{N-1} x_n * exp(-2*pi*i*k*n / N)
        """
        N = len(signal)
        dft_result = []
        for k in range(N):
            s = 0j
            for n in range(N):
                angle = -2.0 * math.pi * k * n / N
                s += signal[n] * cmath.exp(complex(0, angle))
            dft_result.append({
                "freq_bin": k,
                "real": round(s.real, 4),
                "imag": round(s.imag, 4),
                "magnitude": round(abs(s), 4)
            })
        return dft_result
