import math
import cmath

class QuantumInfoCore:
    """Quantum States, Bloch Spheres & Density Matrices"""

    @staticmethod
    def bloch_vector_from_state(alpha_real: float, alpha_imag: float, beta_real: float, beta_imag: float) -> dict:
        """
        Converts pure qubit state |psi> = alpha|0> + beta|1> to Bloch coordinates (u, v, w):
        u = 2 * Re(alpha* * beta)
        v = 2 * Im(alpha* * beta)
        w = |alpha|^2 - |beta|^2
        """
        a = complex(alpha_real, alpha_imag)
        b = complex(beta_real, beta_imag)
        norm_sq = abs(a)**2 + abs(b)**2
        if abs(norm_sq - 1.0) > 1e-4:
            raise ValueError(f"State must be normalized (|alpha|^2 + |beta|^2 = 1). Sum is {norm_sq}")

        ab_star = a.conjugate() * b
        u = 2.0 * ab_star.real
        v = 2.0 * ab_star.imag
        w = abs(a)**2 - abs(b)**2
        radius = math.sqrt(u**2 + v**2 + w**2)
        return {"bloch_u": round(u, 5), "bloch_v": round(v, 5), "bloch_w": round(w, 5), "purity_radius": round(radius, 5)}

    @staticmethod
    def qubit_purity_2x2(rho_00: float, rho_01_real: float, rho_01_imag: float, rho_11: float) -> dict:
        """Computes purity gamma = Tr(rho^2) for a 2x2 density matrix"""
        rho_01 = complex(rho_01_real, rho_01_imag)
        purity = rho_00**2 + rho_11**2 + 2.0 * (abs(rho_01)**2)
        return {"purity": round(purity.real, 5), "is_pure": abs(purity.real - 1.0) < 1e-4}
