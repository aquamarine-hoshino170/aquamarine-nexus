import math
from typing import List

class SovereignKANLinear:
    """
    Kolmogorov-Arnold Network (KAN) Linear Edge Core.
    phi(x) = w_base * silu(x) + sum(c_i * B_i(x))
    """
    def __init__(self, in_features: int, out_features: int, num_grid_intervals: int = 5):
        self.in_features = in_features
        self.out_features = out_features
        self.grid_k = num_grid_intervals

        # Learnable Base weights (SiLU activation scaling)
        scale = 1.0 / math.sqrt(in_features)
        self.w_base = [0.1 * scale for _ in range(out_features * in_features)]

        # Learnable Spline Coefficients: (out_features, in_features, grid_k)
        self.spline_coeffs = [
            0.05 * scale for _ in range(out_features * in_features * self.grid_k)
        ]

    @staticmethod
    def _silu(x: float) -> float:
        # Sigmoid Linear Unit
        return x / (1.0 + math.exp(-max(min(x, 15.0), -15.0)))

    def _rbf_basis(self, x: float, grid_idx: int) -> float:
        """Normalized Gaussian Radial Basis Function as continuous spline proxy."""
        # Grid range [-2.0, 2.0]
        center = -2.0 + (4.0 * grid_idx / float(self.grid_k - 1))
        diff = x - center
        return math.exp(- (diff * diff) * 2.0)

    def forward_vector(self, x: List[float]) -> List[float]:
        """
        Executes KAN Forward Transformation:
        y_j = sum_i [ w_base_{j,i} * SiLU(x_i) + sum_k c_{j,i,k} * B_k(x_i) ]
        """
        y = [0.0] * self.out_features

        for j in range(self.out_features):
            sum_val = 0.0
            for i in range(self.in_features):
                x_i = x[i]
                
                # Base SiLU branch
                base_part = self.w_base[j * self.in_features + i] * self._silu(x_i)

                # Continuous Spline/RBF branch
                spline_part = 0.0
                coeff_offset = (j * self.in_features + i) * self.grid_k
                for k in range(self.grid_k):
                    c_ijk = self.spline_coeffs[coeff_offset + k]
                    basis_val = self._rbf_basis(x_i, k)
                    spline_part += c_ijk * basis_val

                sum_val += (base_part + spline_part)
            y[j] = sum_val

        return y
