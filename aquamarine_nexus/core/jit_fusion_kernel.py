import array
import math
from typing import List, Callable, Dict, Any

class JITFusedKernel:
    """
    Zero-Dependency High-Throughput Fused Execution Kernel.
    Fuses chained scalar operations (e.g. Matmul -> Bias -> GELU/Tanh)
    into a single-pass contiguous memory traversal loop.
    """
    @staticmethod
    def fused_linear_gelu(
        x: array.array, 
        w: array.array, 
        b: array.array, 
        m: int, 
        k: int, 
        n: int
    ) -> array.array:
        """
        Fused Matrix Multiplication + Bias Addition + GELU Activation.
        O(1) memory overhead; computes activations directly during inner reduction.
        """
        out = array.array('d', [0.0] * (m * n))
        
        # Precomputed Gaussian constants for GELU approximation
        sqrt_2_over_pi = math.sqrt(2.0 / math.pi)

        for i in range(m):
            row_offset = i * k
            out_offset = i * n
            for j in range(n):
                acc = b[j]
                for l in range(k):
                    acc += x[row_offset + l] * w[l * n + j]
                
                # Inline Fused GELU: 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
                x_cube = acc * acc * acc
                inner = sqrt_2_over_pi * (acc + 0.044715 * x_cube)
                gelu_val = 0.5 * acc * (1.0 + math.tanh(inner))
                
                out[out_offset + j] = gelu_val

        return out

    @staticmethod
    def fused_vector_layer_norm(
        vec: array.array, 
        gamma: array.array, 
        beta: array.array, 
        dim: int, 
        eps: float = 1e-5
    ) -> array.array:
        """
        Fused Two-Pass Layer Normalization Core.
        """
        out = array.array('d', [0.0] * len(vec))
        num_tokens = len(vec) // dim

        for t in range(num_tokens):
            offset = t * dim
            
            # Pass 1: Mean
            mean = sum(vec[offset + i] for i in range(dim)) / dim
            
            # Pass 2: Variance
            var = sum((vec[offset + i] - mean) ** 2 for i in range(dim)) / dim
            inv_std = 1.0 / math.sqrt(var + eps)
            
            # Pass 3: Normalize and scale
            for i in range(dim):
                normalized = (vec[offset + i] - mean) * inv_std
                out[offset + i] = normalized * gamma[i] + beta[i]

        return out
