import math
import cmath

class QuantumSpinCore:
    """SU(2) Algebra & Pauli Spinor Mechanics"""

    @staticmethod
    def pauli_spin_expectation(alpha_real: float, alpha_imag: float, beta_real: float, beta_imag: float) -> dict:
        """
        Computes expectation values <sigma_x>, <sigma_y>, <sigma_z> for state |psi> = alpha|0> + beta|1>
        """
        a = complex(alpha_real, alpha_imag)
        b = complex(beta_real, beta_imag)
        
        # Normalization verification
        norm_sq = abs(a)**2 + abs(b)**2
        if abs(norm_sq - 1.0) > 1e-4:
            raise ValueError(f"Spinor must be normalized. Current norm^2 = {norm_sq}")

        # <sigma_x> = alpha* beta + beta* alpha = 2 Re(alpha* beta)
        exp_x = 2.0 * (a.conjugate() * b).real
        # <sigma_y> = -i (alpha* beta - beta* alpha) = 2 Im(alpha* beta)
        exp_y = 2.0 * (a.conjugate() * b).imag
        # <sigma_z> = |alpha|^2 - |beta|^2
        exp_z = abs(a)**2 - abs(b)**2

        return {
            "exp_sigma_x": round(exp_x, 6),
            "exp_sigma_y": round(exp_y, 6),
            "exp_sigma_z": round(exp_z, 6)
        }
