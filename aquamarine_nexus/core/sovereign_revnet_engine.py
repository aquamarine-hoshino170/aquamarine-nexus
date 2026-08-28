import math
from typing import List, Tuple

class ReversibleBlock:
    """
    Zero-Memory-Overhead Reversible Residual Block.
    Implements bijective mapping allowing exact reconstruction of inputs
    from outputs during backward propagation without caching activations.
    """
    def __init__(self, half_dim: int):
        self.half_dim = half_dim
        scale = 1.0 / math.sqrt(half_dim)
        
        # Transformation weights for F and G mappings
        self.W_f = [0.05 * ((i + j) % 3) * scale for i in range(half_dim) for j in range(half_dim)]
        self.W_g = [0.05 * ((i - j) % 3) * scale for i in range(half_dim) for j in range(half_dim)]

    def _transform(self, x: List[float], weights: List[float]) -> List[float]:
        """Linear projection with tanh non-linearity."""
        out = [0.0] * self.half_dim
        for i in range(self.half_dim):
            dot = sum(weights[i * self.half_dim + j] * x[j] for j in range(self.half_dim))
            out[i] = math.tanh(dot)
        return out

    def forward(self, x1: List[float], x2: List[float]) -> Tuple[List[float], List[float]]:
        """
        Forward Pass:
        y1 = x1 + F(x2)
        y2 = x2 + G(y1)
        """
        f_x2 = self._transform(x2, self.W_f)
        y1 = [x1[i] + f_x2[i] for i in range(self.half_dim)]

        g_y1 = self._transform(y1, self.W_g)
        y2 = [x2[i] + g_y1[i] for i in range(self.half_dim)]

        return y1, y2

    def inverse(self, y1: List[float], y2: List[float]) -> Tuple[List[float], List[float]]:
        """
        Exact Analytical Reverse Reconstruction:
        x2 = y2 - G(y1)
        x1 = y1 - F(x2)
        """
        g_y1 = self._transform(y1, self.W_g)
        x2 = [y2[i] - g_y1[i] for i in range(self.half_dim)]

        f_x2 = self._transform(x2, self.W_f)
        x1 = [y1[i] - f_x2[i] for i in range(self.half_dim)]

        return x1, x2

class SovereignDeepRevNet:
    """
    Arbitrarily Deep Reversible Network operating in constant O(1) activation RAM.
    """
    def __init__(self, total_dim: int = 8, num_layers: int = 10):
        if total_dim % 2 != 0:
            raise ValueError("total_dim must be even to split into (x1, x2)")
        self.total_dim = total_dim
        self.half_dim = total_dim // 2
        self.num_layers = num_layers
        self.layers = [ReversibleBlock(self.half_dim) for _ in range(num_layers)]

    def forward(self, x: List[float]) -> Tuple[List[float], List[float]]:
        x1 = x[:self.half_dim]
        x2 = x[self.half_dim:]

        for layer in self.layers:
            x1, x2 = layer.forward(x1, x2)

        return x1, x2

    def reconstruct_input(self, y1: List[float], y2: List[float]) -> List[float]:
        """Reconstructs original input by propagating backwards through inverted dynamics."""
        curr_y1, curr_y2 = y1, y2
        for layer in reversed(self.layers):
            curr_y1, curr_y2 = layer.inverse(curr_y1, curr_y2)

        return curr_y1 + curr_y2
