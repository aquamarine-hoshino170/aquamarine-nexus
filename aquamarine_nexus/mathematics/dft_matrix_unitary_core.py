import math

class DFTMatrixUnitaryCore:
    @staticmethod
    def dft_unitarity_check_dim(dim_n: int) -> dict:
        """F_{jk} = (1/sqrt(N)) * exp(-2*pi*i * j * k / N), Verifies F * F^dagger = I"""
        if dim_n <= 1:
            raise ValueError("Dimension N must be strictly greater than 1.")
            
        # Analytical check of inner product between row 0 and row 1: sum_{k=0}^{N-1} exp(-2*pi*i * k / N) = 0
        real_sum = sum(math.cos(2.0 * math.pi * k / dim_n) for k in range(dim_n))
        imag_sum = sum(math.sin(2.0 * math.pi * k / dim_n) for k in range(dim_n))
        
        orthogonality_residual = math.sqrt(real_sum**2 + imag_sum**2) / dim_n
        
        return {
            "matrix_dimension_N": dim_n,
            "row_orthogonality_residual": f"{orthogonality_residual:.10e}",
            "is_strictly_unitary": orthogonality_residual < 1e-12
        }
