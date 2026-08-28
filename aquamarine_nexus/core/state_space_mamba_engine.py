import math
import array
from typing import List, Tuple, Dict, Any

class SelectiveStateSpaceCore:
    """
    Zero-Dependency High-Throughput Selective State Space (SSM) Kernel.
    Linear-time O(N) sequence modeling replacing quadratic self-attention:
    h_t = A_bar * h_{t-1} + B_bar * x_t
    y_t = C * h_t + D * x_t
    """

    @staticmethod
    def selective_scan_1d(
        x: List[float],
        delta: List[float],
        A_diag: List[float],
        B: List[float],
        C: List[float],
        D: float = 0.0
    ) -> List[float]:
        """
        Executes selective parameter discretization and state scan in O(L * D_state).
        """
        L = len(x)
        d_state = len(A_diag)
        y = [0.0] * L
        h = [0.0] * d_state

        for t in range(L):
            x_t = x[t]
            dt = delta[t]

            # Discretize continuous matrices via zero-order hold (ZOH)
            # A_bar = exp(dt * A), B_bar = dt * B
            for i in range(d_state):
                a_bar = math.exp(dt * A_diag[i])
                b_bar = dt * B[i]
                
                # Hidden state evolution
                h[i] = a_bar * h[i] + b_bar * x_t

            # Output projection: y_t = sum(C_i * h_i) + D * x_t
            y_t = sum(C[i] * h[i] for i in range(d_state)) + D * x_t
            y[t] = y_t

        return y

    @staticmethod
    def parallel_associative_scan(
        a_elements: List[float], 
        b_elements: List[float]
    ) -> List[float]:
        """
        Prefix associative scan operator for hardware-parallel SSM evaluation:
        (a1, b1) o (a2, b2) = (a1 * a2, a2 * b1 + b2)
        """
        n = len(a_elements)
        result = [0.0] * n
        if n == 0:
            return result

        curr_a = a_elements[0]
        curr_b = b_elements[0]
        result[0] = curr_b

        for i in range(1, n):
            curr_b = a_elements[i] * curr_b + b_elements[i]
            curr_a = curr_a * a_elements[i]
            result[i] = curr_b

        return result
